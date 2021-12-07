# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-job-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Plugin for the Storm Job to enable experiments execution on REANA instances."""

import os

#
# General
#
DOCKER_REPOSITORY_PREFIX = "storm"
DOCKER_IMAGE_PREFIX = "storm-job-{uuid}"

#
# Reprozip module
#
REPROZIP_PROXY_DOCKER_IMAGE_TAG = "storm/storm-reprozip-proxy:latest"
REPROZIP_INCLUDE_USER_DEFINITION = int(os.getenv("REPROZIP_INCLUDE_USER_DEFINITION", 1))
