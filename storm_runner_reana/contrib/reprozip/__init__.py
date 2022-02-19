# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-runner-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_runner_reana.contrib.reprozip.services.serial import (
    PluginService as PluginServiceSerialExecution,
)


def init_contrib(service_register):
    """Initialize the Reana-Reprozip contrib services."""
    service_register[PluginServiceSerialExecution.id] = PluginServiceSerialExecution
