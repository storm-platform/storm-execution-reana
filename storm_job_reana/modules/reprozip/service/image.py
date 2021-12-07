# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-job-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pathlib import Path

from storm_job_reana.config import REPROZIP_PROXY_DOCKER_IMAGE_TAG


def create_proxy_dockerfile(dockerfile_path: Path, bundle_path: Path):
    """Create a Dockerfile with the Reprozip proxy tools.

    Args:
        dockerfile_path (pathlib.Path): Absolute path to the Dockerfile file that will be generated.

        bundle_path (pathlib.Path): Absolute path to the reprozip bundle file that will be copied in the Dockerfile.
    Returns:
        pathlib.Path: Absolute path to the Dockerfile.
    """
    with open(dockerfile_path, "w") as ofile:
        dockerfile_content = """
            FROM {PROXY_IMAGE}
            
            # Copying files
            COPY {BUNDLE_FILE} /opt/input/package.rpz
        """.format(
            PROXY_IMAGE=REPROZIP_PROXY_DOCKER_IMAGE_TAG, BUNDLE_FILE=bundle_path
        )

        ofile.write("\n".join([i.strip() for i in dockerfile_content.split("\n")]))
    return dockerfile_path


__all__ = "create_proxy_dockerfile"
