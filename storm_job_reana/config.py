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
DOCKER_IMAGE_PREFIX = "storm-job-{uuid}"
DOCKER_REPOSITORY_PREFIX = "storm"

#
# Reprozip module
#
REPROZIP_INCLUDE_USER_DEFINITION = int(os.getenv("REPROZIP_INCLUDE_USER_DEFINITION", 1))
