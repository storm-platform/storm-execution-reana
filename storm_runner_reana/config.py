# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-runner-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Plugin for the Storm Runner to enable experiments execution on REANA instances."""

STORM_RUNNER_REANA_DOCKER_REPOSITORY = "stormproject"
"""Docker Image repository."""

STORM_RUNNER_REANA_DOCKER_IMAGE_PREFIX = "storm-runner-{uuid}"
"""Docker Image name prefix."""

STORM_RUNNER_REANA_REPROZIP_PROXY_IMAGE = "stormproject/storm-reprozip-proxy:latest"
"""Docker Image of the Storm Reprozip Proxy."""
