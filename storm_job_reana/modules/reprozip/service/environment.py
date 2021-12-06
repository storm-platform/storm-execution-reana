# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-job-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import uuid
import docker


from ....config import DOCKER_IMAGE_PREFIX, DOCKER_REPOSITORY_PREFIX

client = docker.from_env()


def _generate_uuid():
    return str(uuid.uuid4())


def build_vertex_environment(build_context):
    tagname = DOCKER_IMAGE_PREFIX.format(uuid=_generate_uuid())
    image_name = f"{DOCKER_REPOSITORY_PREFIX}/{tagname}:latest"

    image, _ = client.images.build(
        path=build_context,
        tag=image_name,
        nocache=True,
        rm=True,
        quiet=False,
    )

    return image_name
