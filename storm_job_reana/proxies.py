# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-job-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from flask import current_app
from werkzeug.local import LocalProxy

current_storm_job_reana = LocalProxy(lambda: current_app.extensions["storm-job-reana"])
"""Helper proxy to get the current Storm Job Reana extension."""

docker_repository = LocalProxy(
    lambda: current_app.config["STORM_JOB_REANA_DOCKER_REPOSITORY"]
)
"""Docker Image repository."""

docker_image_prefix = LocalProxy(
    lambda: current_app.config["STORM_JOB_REANA_DOCKER_IMAGE_PREFIX"]
)
"""Docker Image name prefix."""

docker_image_tag_reprozip_proxy = LocalProxy(
    lambda: current_app.config["STORM_JOB_REANA_REPROZIP_PROXY_IMAGE"]
)
"""Docker Image of the Storm Reprozip Proxy."""
