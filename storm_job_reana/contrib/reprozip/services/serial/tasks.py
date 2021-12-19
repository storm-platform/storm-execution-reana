# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-job-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import json
import shutil
import tempfile

from pydash import py_

from pathlib import Path
from rpaths import Path as rPath

from celery import shared_task

from reana_client.api import client as reana_client
from reprounzip.common import RPZPack, load_config

from storm_graph import graph_manager_from_json
from storm_compendium.compendium.records.api import CompendiumRecord

from storm_job_reana.environment.docker import (
    DockerImageCacheHandler,
    DockerImageIdentifierProvider,
)

from storm_job_reana.contrib.reprozip.image import create_proxy_dockerfile
from storm_reprozip_proxy.helper.reprozip import reprozip_extract_bundle_io

from storm_job_reana.helper.records import pass_records
from storm_job_reana.helper.reana import pass_reana_token
from storm_job_reana.environment.decorator import pass_docker_handler


@shared_task
@pass_reana_token
@pass_records
@pass_docker_handler
def service_task(job, pipeline, reana_access_token, docker_handler):
    """Generate Reana serial execution tasks from the Storm pipelines.

    Args:
        job (storm_job.job.models.api.ExecutionJob): Record API to handle the executed job database record.

        pipeline (storm_pipeline.pipeline.records.api.ResearchPipeline): Record API to handle the pipeline
                                                                         database record.

        reana_access_token (str): Access token to access the Reana Services.

        docker_handler (storm_job_reana.environment.docker.DockerEnvironmentHandler): Object to allow the manipulation
                                                                                      required Docker Daemon.
    Return:
        None: The task will be send to Reana cluster and the local database will be update with the processing status.
    """

    # Load the defined pipeline.
    graph_manager = graph_manager_from_json({"graph": pipeline.graph})

    # Reana description for each vertex record.
    reana_steps = []

    # Workflow definition files
    workflow_inputs = []
    workflow_outputs = []

    # Workflow outside input files
    files_to_upload = []

    # Mapping files
    mapping_files_description = []

    temporary_directory = Path(tempfile.mkdtemp())
    for vertex in graph_manager.vertices:
        #
        # Vertex configurations
        #

        # Load vertex record
        vertex_record = CompendiumRecord.pid.resolve(vertex.name)
        vertex_uuid = str(vertex_record.id)

        vertex_directory = temporary_directory / str(vertex_record.id)
        vertex_directory.mkdir()

        # Configuration files load.
        config_file = rPath((vertex_directory / "config.yml").as_posix())

        # Vertex environment bundle
        environment_file_key = py_.get(
            vertex_record.metadata, "execution.environment.meta.files.key"
        )

        environment_file = vertex_record.files[environment_file_key]
        reprozip_bundle_file = RPZPack(environment_file.file.uri)

        # Load bundle configurations
        reprozip_bundle_file.extract_config(config_file)
        config = load_config(config_file, True)

        #
        # Input/Output definition
        #
        map_path_to_posix_operation = lambda file: (
            Path(file["location"]) / file["file"].path.name.decode()
        ).as_posix()

        inputs, outputs = reprozip_extract_bundle_io(config)

        # Input files
        map_file_to_dict_operation = lambda file: {
            "file": file,
            "checksum": vertex_record.files.entries[
                file.path.name.decode()
            ].file.file_model.checksum.replace("md5:", ""),
        }

        inputs = py_.map(
            py_.filter(
                lambda x: x != config.inputs_outputs.get("arg")
                if config.inputs_outputs.get("arg")
                else True,
                inputs,
            ),
            map_file_to_dict_operation,
        )

        # defining the `file` location in the execution environment (based on the reproducible bundle)
        inputs = [
            {
                **input_file_definition,
                "location": Path("data")
                / vertex.name
                / "raw_data"
                / (
                    str(inputs[0]["file"].path.parent)[1:]
                    if str(inputs[0]["file"].path.parent)[0] == "/"
                    else str(inputs[0]["file"].path.parent)
                ),
            }
            for input_file_definition in inputs
        ]

        # Output files
        outputs = py_.map(
            outputs,
            map_file_to_dict_operation,
        )

        outputs = [
            {
                **output_file_definition,
                "location": Path("data")
                / vertex.name
                / "derived_data"
                / (
                    str(outputs[0]["file"].path.parent)[1:]
                    if str(outputs[0]["file"].path.parent)[0] == "/"
                    else str(outputs[0]["file"].path.parent)
                ),
            }
            for output_file_definition in outputs
        ]

        # Check if the vertex required input files is defined in the predecessor vertices.
        checksum_comparator = lambda x, y: x["checksum"] == y["checksum"]

        already_defined_input_files = py_.intersection_with(
            inputs,
            workflow_outputs,
            comparator=checksum_comparator,
        )

        if already_defined_input_files:
            mapping_files_description.append(
                [
                    {
                        "source": py_.chain(workflow_outputs)
                        .filter_(lambda x: x["checksum"] == defined_file["checksum"])
                        .map(map_path_to_posix_operation)
                        .head()
                        .value(),
                        "target": str(defined_file["file"].path),
                        "executionId": vertex.name,
                        "type": "input",
                    }
                    for defined_file in already_defined_input_files
                ]
            )

        required_files = py_.difference_with(
            inputs, already_defined_input_files, comparator=checksum_comparator
        )

        if required_files:  # load the files reference to upload
            checksum_extract_operation = lambda file: file["checksum"]

            md5_adapter_operation = lambda obj: obj.file.file_model.checksum.replace(
                "md5:", ""
            )

            # search for the files with the same checksum
            required_files = py_.map(
                required_files,
                lambda obj: {
                    **obj,
                    **{
                        "file_record": py_.find(
                            list(vertex_record.files.entries.values()),
                            md5_adapter_operation
                            in py_.map(
                                required_files,
                                checksum_extract_operation,
                            ),
                        )
                    },
                },
            )

            required_files = py_.filter_(
                required_files,
                checksum_extract_operation
                in py_.map(
                    list(vertex_record.files.entries.values()),
                    md5_adapter_operation,
                ),
            )

            # define the required files in the mapping file
            mapping_files_description.append(
                [
                    {
                        "source": map_path_to_posix_operation(required_file),
                        "target": str(required_file["file"].path),
                        "executionId": vertex.name,
                        "type": "input",
                    }
                    for required_file in required_files
                ]
            )

        # mapping the output files
        mapping_files_description.append(
            [
                {
                    "source": str(output_file["file"].path),
                    "target": map_path_to_posix_operation(output_file),
                    "executionId": vertex.name,
                    "type": "output",
                }
                for output_file in outputs
            ]
        )

        files_to_upload.extend(required_files)

        workflow_inputs.extend(inputs)
        workflow_outputs.extend(outputs)

        #
        # Environment
        #
        try:
            vertex_environment = DockerImageCacheHandler.get_record(
                compendium_id=vertex_uuid
            )

            image_name = vertex_environment.image_name
        except:
            # If there are no previous records in the database,
            # then the vertex environment build is performed.
            environment_build_directory = vertex_directory / "docker-build"
            environment_build_directory.mkdir()

            dockerfile_path = create_proxy_dockerfile(
                environment_build_directory / "Dockerfile",
                Path(environment_file.file.uri),
            )

            # Build the environment image
            image_name = DockerImageIdentifierProvider.generate(vertex_uuid)

            # In the `path` argument, it is assumed that the directory where the
            # application is running has access to the Invenio data directory.
            docker_handler.build_image(
                tag=image_name,
                path=Path.cwd().as_posix(),
                dockerfile=dockerfile_path.as_posix(),
            )
            docker_handler.push_image(image_name)

            # If no errors have occurred, then the data is saved in the cache:
            DockerImageCacheHandler.create(
                commit=True,
                service="DockerHub",  # Currently, DockerHub is the only supported service.
                image_name=image_name,
                compendium_id=vertex_uuid,
            )

        # Reana serial step definition
        reana_step_commands = f"""
                    /storm-reprozip-parser {vertex.name} file_mapping_specification.json input
                        && /busybox cat /cmd | /busybox sh
                        && /busybox mkdir -p data/{vertex.name}/derived_data
                        && /storm-reprozip-parser {vertex.name} file_mapping_specification.json output
                    """

        reana_steps.append(
            {
                "name": vertex.name,
                "environment": image_name,
                "commands": [
                    " ".join([i.strip() for i in reana_step_commands.split("\n")])
                ],
            }
        )

    #
    # Vertex files operations description
    #
    filter_operation = lambda files, type_: py_.filter_(
        files, lambda x: x["type"] == type_
    )

    mapping_files_description = py_.flatten(mapping_files_description)
    vertex_files_description = temporary_directory / "file_mapping_specification.json"

    with open(vertex_files_description, "w") as ofile:
        json.dump(
            {
                "inputs": filter_operation(mapping_files_description, "input"),
                "outputs": filter_operation(mapping_files_description, "output"),
            },
            ofile,
        )

    #
    # Reana workflow specification
    #

    # Serial definition file
    map_operation = lambda files: py_.map(
        files,
        lambda x: str(x["location"] / x["file"].path.name.decode()),
    )

    reana_serial_workflow = {
        "version": "0.6.0",
        "workflow": {"type": "serial", "specification": {"steps": reana_steps}},
        "outputs": {"files": map_operation(workflow_outputs)},
        "inputs": {"files": map_operation(files_to_upload)},
    }

    # creating the workflow
    workflow_name = f"storm-job-{str(pipeline.id)}"
    reana_client.create_workflow(
        reana_serial_workflow, workflow_name, reana_access_token
    )

    # Upload the required files
    py_.map(
        files_to_upload,
        lambda x: reana_client.upload_file(
            workflow_name,
            x["file_record"].get_stream("r"),
            str(x["location"] / x["file"].path.name.decode()),
            reana_access_token,
        ),
    )

    # Upload the file mapping
    reana_client.upload_file(
        workflow_name,
        vertex_files_description.open("r"),
        "file_mapping_specification.json",
        reana_access_token,
    )

    # Removing files
    shutil.rmtree(temporary_directory)
