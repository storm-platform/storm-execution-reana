# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-execution-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from pathlib import Path

from storm_commons.template import render_template
from storm_execution_reana.proxies import docker_image_tag_reprozip_proxy


def create_proxy_dockerfile(dockerfile_path: Path, bundle_path: Path):
    """Create a Dockerfile with the Reprozip proxy tools.

    Args:
        dockerfile_path (pathlib.Path): Absolute path to the Dockerfile file that will be generated.

        bundle_path (pathlib.Path): Absolute path to the reprozip bundle file that will be copied in the Dockerfile.
    Returns:
        pathlib.Path: Absolute path to the Dockerfile.
    """
    with open(dockerfile_path, "w") as ofile:
        dockerfile_content = render_template(
            "Dockerfile",
            "storm_execution_reana.contrib.reprozip",
            "templates",
            proxy_image=docker_image_tag_reprozip_proxy,
            bundle_file=bundle_path,
        )

        ofile.write(dockerfile_content)
    return dockerfile_path


__all__ = "create_proxy_dockerfile"
