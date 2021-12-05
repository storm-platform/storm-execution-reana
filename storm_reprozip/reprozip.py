# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-reprozip is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from itertools import chain

from reprounzip.common import RPZPack
from reprounzip.utils import join_root

from rpaths import Path, PosixPath


def reprozip_extract_bundle_input(config):
    """Extract reprozip bundle inputs."""

    workingdir = config.runs[0]["workingdir"]

    # filtering by working dir
    inputs = []
    for file_key in config.inputs_outputs:

        input_output_file = config.inputs_outputs[file_key]

        # verify if file is within working dir
        if input_output_file.path.lies_under(workingdir):

            # verify if file is a input (written by nobody)
            if len(input_output_file.write_runs) == 0:
                # yes! this is a input file
                inputs.append(input_output_file)
    return inputs


def reprozip_extract_rpzfiles(reprozip_bundle: RPZPack, config, output_file):
    """Extract `rpzfiles` from reprozip bundle.

    Note:
        This function is based on `reprounzip-docker`: https://github.com/VIDA-NYU/reprozip/blob/929af95f83c37ee4634475d80711ea6c55413f90/reprounzip-docker/reprounzip/unpackers/docker.py
    """

    runs, packages, other_files = config

    missing_packages = [pkg for pkg in packages if pkg.packfiles]
    # packages = [pkg for pkg in packages if not pkg.packfiles]

    paths = set()
    pathlist = []

    missing_files = chain.from_iterable(pkg.files for pkg in missing_packages)

    data_files = reprozip_bundle.data_filenames()
    listoffiles = list(chain(other_files, missing_files))

    for f in listoffiles:
        if f.path.unicodename in ("resolv.conf", "hosts") and (
            f.path.lies_under("/etc")
            or f.path.lies_under("/run")
            or f.path.lies_under("/var")
        ):
            continue

        path = PosixPath("/")
        for c in reprozip_bundle.remove_data_prefix(f.path).components:
            path = path / c
            if path in paths:
                continue
            paths.add(path)  # ; print(path)
            if path in data_files:
                if path != "/etc":
                    pathlist.append(path)
            else:
                print(f"missing file {path}")
    reprozip_bundle.close()
    with Path(output_file).open("wb") as filelist:
        for p in pathlist:
            filelist.write(join_root(PosixPath(""), p).path)
            filelist.write(b"\0")


__all__ = ("reprozip_extract_rpzfiles", "reprozip_extract_bundle_input")
