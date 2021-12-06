# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-job-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


import click
from .cmd.commands import reprozip_proxy_run


@click.group(name="reprozip")
def reprozip():
    """Reprozip Job execution management commands."""


@reprozip.command(name="run")
@click.option("--bundle", required=True)
@click.option("--input-file", multiple=True)
@click.option("--input-name", multiple=True)
def reprozip_run(bundle, input_file, input_name):
    reprozip_proxy_run(bundle, input_file, input_name)


def add_command(click_instance):
    """Add the command in the click instance."""

    click_instance.add_command(reprozip)
