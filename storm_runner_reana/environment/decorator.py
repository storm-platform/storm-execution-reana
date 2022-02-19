# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-runner-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from functools import wraps

from storm_runner_reana.environment.docker import DockerEnvironmentHandler


def pass_docker_handler(f):
    """Decorator to pass a Docker environment handler object to the function."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            docker_handler = DockerEnvironmentHandler()
        except:
            raise RuntimeError("Error on load the Docker Environment Handler.")

        return f(docker_handler=docker_handler, *args, **kwargs)

    return wrapper
