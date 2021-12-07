# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-job-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import os
import click

import shutil
import tempfile

from pathlib import Path
from rpaths import Path as rPath

from reprounzip.common import RPZPack, load_config

from storm_job_reana.modules.reprozip.reprozip import (
    reprozip_extract_rpzfiles,
    reprozip_extract_bundle_io,
)

from storm_job_reana.modules.reprozip.cmd.busybox import (
    BusyBoxWrapperBuilder,
    busybox_bundle_cmd,
)

from storm_job_reana.config import REPROZIP_INCLUDE_USER_DEFINITION


def reprozip_proxy_run(bundle, input_file, input_name):
    proxy_path = Path.cwd()
    proxy_path.mkdir(exist_ok=True)

    #
    # Define reprozip bundle.
    #
    reprozip_bundle = RPZPack(bundle)

    #
    # Configuration files load.
    #
    config_dir = Path(tempfile.mkdtemp())
    config_file = rPath((config_dir / "config.yml").as_posix())

    #
    # Extract and load.
    #
    reprozip_bundle.extract_config(config_file)
    config = load_config(config_file, True)

    click.echo(f"Temporary directory: {proxy_path.as_posix()}")
    os.makedirs(proxy_path, exist_ok=True)

    #
    # Data Files.
    #
    click.echo("Extract data files...")
    bundle_data = rPath((proxy_path / "data.tgz").as_posix())

    reprozip_bundle.copy_data_tar(bundle_data)

    #
    # RPZ Files.
    #
    click.echo("Generating rpz-files...")
    rpzfiles_path = rPath((proxy_path / "rpz-files.list").as_posix())

    reprozip_extract_rpzfiles(reprozip_bundle, config, rpzfiles_path)

    #
    # Define Busybox shell command.
    #
    click.echo("Preparing busybox commands...")
    cmds = busybox_bundle_cmd(config.runs, REPROZIP_INCLUDE_USER_DEFINITION)

    busybox_wrapper = (
        BusyBoxWrapperBuilder()
        .add_cmds(cmds)
        .add_bundle_data(bundle_data)
        .add_rpzfiles(rpzfiles_path)
    )

    #
    # Busybox linking.
    #
    click.echo("Extract busybox...")
    # Warning! The command below overwrites all files in your local environment.
    busybox_wrapper.link_environment()

    #
    # Files replace.
    #
    click.echo("Check and replace input files...")
    inputs, _ = reprozip_extract_bundle_io(config)
    user_defined_inputs = list(zip(input_name, input_file))

    if len(inputs) == 0:
        click.echo(" The experiment don't have input files...")
    else:

        if len(input_name) != len(input_file):
            click.echo(
                " To replace files input-names and input-files should have the same length"
            )
        else:

            if user_defined_inputs:
                click.echo(" Replacing files")

                for filename, filepath in user_defined_inputs:
                    # filter list by filename
                    selected_file_to_replace = list(
                        filter(lambda x: x["name"] == filename, inputs)
                    )

                    if selected_file_to_replace:
                        click.echo(f"  > {filename}")
                        selected_file_to_replace = selected_file_to_replace[0]

                        shutil.copy(filepath, selected_file_to_replace["path"])

    click.echo("Generating experiment command file...")
    busybox_wrapper.create_cmd_file(proxy_path)


__all__ = "reprozip_proxy_run"
