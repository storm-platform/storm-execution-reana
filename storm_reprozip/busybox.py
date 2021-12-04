# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-reprozip is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import os
from pathlib import Path

from reprounzip.utils import iteritems, irange

from reprounzip.unpackers.common import shell_escape
from reprounzip.unpackers.common.x11 import X11Handler


class BusyBoxWrapperBuilder:
    """Busybox wrapper for reprozip operations."""

    def __init__(self, cmds=None, rpzfiles=None, bundle_data=None):
        self._cmds = cmds
        self._rpzfiles = rpzfiles
        self._bundle_data = bundle_data

    def add_cmds(self, cmds):
        """Add cmd from bundle."""

        self._cmds = cmds

        return self

    def add_bundle_data(self, bundle_data):
        """Add bundle data file."""

        self._bundle_data = bundle_data

        return self

    def add_rpzfiles(self, rpzfiles):
        """Add RPZFiles from bundle."""
        self._rpzfiles = rpzfiles

        return self

    def link_environment(self):
        """Link package data to the local operational system.

        Warning:
            This function changes all the directories in your environment. Make sure you are
            running it in a safe and controlled environment.
        """

        rpzdata = self._bundle_data
        rpzfiles = self._rpzfiles

        os.chdir("/")
        command = f"""
        cd / && tar zpxf {rpzdata} -U --recursive-unlink --numeric-owner --strip=1 --null -T {rpzfiles} || /busybox echo "TAR reports errors, this might or might not prevent the execution to run"
        """.strip()

        os.system(command)

    def create_cmd_file(self, output_directory: str):
        """Create a file with the busybox cmd commands (To run the experiments reproduction)."""

        cmdfile = Path(output_directory) / "cmd"
        with open(cmdfile, "w") as file:
            file.write(self._cmds)


def busybox_bundle_cmd(bundle_runs, include_user_definition: bool = True):
    """Prepare the busybox cmd to run reprozip bundle.

    Args:
        bundle_runs (List): Bundle executions

        include_user_definition (bool): Flag to enable the user definition in the generated command.

    Note:
        This function is based on `reprounzip-docker`: https://github.com/VIDA-NYU/reprozip/blob/929af95f83c37ee4634475d80711ea6c55413f90/reprounzip-docker/reprounzip/unpackers/docker.py
    """

    selected_runs = list(irange(len(bundle_runs)))

    hostname = bundle_runs[selected_runs[0]].get("hostname", "reprounzip")
    x11 = X11Handler(False, ("local", hostname), None)

    cmds = []
    for run_number in selected_runs:
        run = bundle_runs[run_number]

        cmd = "cd %s && " % shell_escape(run["workingdir"])
        cmd += "/busybox env -i "
        environ = x11.fix_env(run["environ"])

        cmd += " ".join(
            "%s=%s" % (shell_escape(k), shell_escape(v)) for k, v in iteritems(environ)
        )
        cmd += " "

        # create docker cmd!
        argv = [run["binary"]] + run["argv"][1:]
        cmd += " ".join(shell_escape(a) for a in argv)

        # preparing the shell command
        cmd = "/busybox sh -c %s" % (shell_escape(cmd))

        # defining user and group id
        if include_user_definition:
            uid = run.get("uid", 1000)
            gid = run.get("gid", 1000)

            cmd = ("/rpzsudo '#%d' '#%d'" % (uid, gid)) + cmd

        cmds.append(cmd)
    cmds = x11.init_cmds + cmds
    cmds = " && ".join(cmds)

    return cmds


__all__ = ("BusyBoxWrapperBuilder", "busybox_bundle_cmd")
