# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-execution-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask import current_app
from werkzeug.local import LocalProxy

current_storm_execution_reana = LocalProxy(
    lambda: current_app.extensions["storm-execution-reana"]
)
"""Helper proxy to get the current Storm Execution Reana extension."""

docker_repository = LocalProxy(
    lambda: current_app.config["STORM_EXECUTION_REANA_DOCKER_REPOSITORY"]
)
"""Docker Image repository."""

docker_image_prefix = LocalProxy(
    lambda: current_app.config["STORM_EXECUTION_REANA_DOCKER_IMAGE_PREFIX"]
)
"""Docker Image name prefix."""

docker_image_tag_reprozip_proxy = LocalProxy(
    lambda: current_app.config["STORM_EXECUTION_REANA_REPROZIP_PROXY_IMAGE"]
)
"""Docker Image of the Storm Reprozip Proxy."""
