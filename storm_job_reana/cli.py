# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-job-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import click
from importlib import import_module


MODULES = ["storm_job_reana.modules.reprozip.cli"]


def init_cli():
    """Create a new cli"""

    @click.group(name="storm-job-reana")
    @click.version_option()
    def storm_job_reana():
        """Storm Job Reana base CLI."""

    # adding view modules
    for module in MODULES:
        mod = import_module(module)
        mod.add_command(storm_job_reana)

    return storm_job_reana


cli = init_cli()
