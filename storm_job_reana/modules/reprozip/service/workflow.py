# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-job-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import uuid
import json
import shutil
import tempfile

from pydash import py_

from pathlib import Path
from rpaths import Path as rPath

from reana_client.api import client as reana_client
from reprounzip.common import RPZPack, load_config

from storm_graph import graph_manager_from_json
from storm_pipeline.pipeline.records.api import ResearchPipeline
from storm_compendium.compendium.records.api import CompendiumRecord


from .environment import (
    client,
    build_vertex_environment,
)
from ..reprozip import reprozip_extract_bundle_io


def create_serial_workflow_spec_from_pipeline(pipeline_id: str, access_token: str):
    """"""

    #
    # Load the defined pipeline.
    #
    current_pipeline = ResearchPipeline.pid.resolve(pipeline_id)
    graph_manager = graph_manager_from_json({"graph": current_pipeline.graph})

    #
    # Description for each vertex record.
    #
    reana_steps = []

    # Workflow definition files
    workflow_inputs = []
    workflow_outputs = []

    # Workflow outside input files
    files_to_upload = []

    # Mapping files
    mapping_files_description = []

    for vertex in graph_manager.vertices:

        #
        # Workflow definition
        #

        # Load vertex record
        vertex_record = CompendiumRecord.pid.resolve(vertex.name)

        # Configuration files load.
        config_dir = Path(tempfile.mkdtemp())
        config_file = rPath((config_dir / "config.yml").as_posix())

        # Vertex environment bundle
        environment_file_key = vertex_record.metadata["execution"]["environment"][
            "meta"
        ]["files"]["key"]

        environment_file = vertex_record.files[environment_file_key]
        reprozip_bundle_file = RPZPack(environment_file.file.uri)

        # Load bundle configurations
        reprozip_bundle_file.extract_config(config_file)
        config = load_config(config_file, True)

        #
        # Input/Output definition
        #
        inputs, outputs = reprozip_extract_bundle_io(config)

        # Input files
        inputs = list(
            map(
                lambda o: {
                    "file": o,
                    "checksum": vertex_record.files.entries[
                        o.path.name.decode()
                    ].file.file_model.checksum.replace("md5:", ""),
                },
                filter(
                    lambda x: x != config.inputs_outputs.get("arg")
                    if config.inputs_outputs.get("arg")
                    else True,
                    inputs,
                ),
            )
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
        outputs = list(
            map(
                lambda o: {
                    "file": o,
                    "checksum": vertex_record.files.entries[
                        o.path.name.decode()
                    ].file.file_model.checksum.replace("md5:", ""),
                },
                outputs,
            )
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
                        .map(
                            lambda x: (
                                Path(x["location"]) / x["file"].path.name.decode()
                            ).as_posix()
                        )
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
            # search for the files with the same checksum
            required_files = py_.map(
                required_files,
                lambda x: {
                    **x,
                    **{
                        "file_record": py_.find(
                            list(vertex_record.files.entries.values()),
                            lambda y: y.file.file_model.checksum.replace("md5:", "")
                            in py_.map(
                                required_files,
                                lambda z: z["checksum"],
                            ),
                        )
                    },
                },
            )

            required_files = py_.filter_(
                required_files,
                lambda z: z["checksum"]
                in py_.map(
                    list(vertex_record.files.entries.values()),
                    lambda x: x.file.file_model.checksum.replace("md5:", ""),
                ),
            )

            # define the required files in the mapping file
            mapping_files_description.append(
                [
                    {
                        "source": (
                            Path(required_file["location"])
                            / required_file["file"].path.name.decode()
                        ).as_posix(),
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
                    "target": (
                        Path(output_file["location"])
                        / output_file["file"].path.name.decode()
                    ).as_posix(),
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

        # Copy the bundle file (FIXME: Maybe create a symbolic link ?)
        shutil.copy(
            environment_file.file.uri,
            (Path(__file__).parent / "data/package.rpz").as_posix(),
        )

        # Build the environment image
        generated_image = build_vertex_environment(
            (Path(__file__).parent / "data").as_posix()
        )

        # Send to Dockerhub (FIXME: do we should freeze this registry here ?)
        # ToDo: Save the image reference in a database to avoid multiple build/publish.
        client.images.push(generated_image)

        # Reana serial step definition
        reana_steps.append(
            {
                "name": vertex.name,
                "environment": generated_image,
                "commands": [
                    f"/parser {vertex.name} file_mapping_specification.json input && /busybox cat /cmd | /busybox sh && /busybox mkdir -p data/{vertex.name}/derived_data && /parser {vertex.name} file_mapping_specification.json output"
                ],
            }
        )

    # creating the final reana serial definition file
    reana_serial_workflow = {
        "version": "0.6.0",
        "workflow": {"type": "serial", "specification": {"steps": reana_steps}},
        "outputs": {
            "files": py_.map(
                workflow_outputs,
                lambda x: str(x["location"] / x["file"].path.name.decode()),
            )
        },
        "inputs": {
            "files": py_.map(
                files_to_upload,
                lambda x: str(x["location"] / x["file"].path.name.decode()),
            )
        },
    }

    # creating the mapping specification file
    mapping_files_description = py_.flatten(mapping_files_description)

    with open("file_mapping_specification.json", "w") as ofile:
        json.dump(
            {
                "inputs": py_.filter_(
                    mapping_files_description, lambda x: x["type"] == "input"
                ),
                "outputs": py_.filter_(
                    mapping_files_description, lambda x: x["type"] == "output"
                ),
            },
            ofile,
        )

    # creating the workflow
    workflow_name = f"test-{str(uuid.uuid4())}"
    reana_client.create_workflow(reana_serial_workflow, workflow_name, access_token)

    # Upload the required files
    py_.map(
        files_to_upload,
        lambda x: reana_client.upload_file(
            workflow_name,
            x["file_record"].get_stream("r"),
            str(x["location"] / x["file"].path.name.decode()),
            access_token,
        ),
    )

    # Upload the file mapping
    reana_client.upload_file(
        workflow_name,
        open("file_mapping_specification.json"),
        "file_mapping_specification.json",
        access_token,
    )
