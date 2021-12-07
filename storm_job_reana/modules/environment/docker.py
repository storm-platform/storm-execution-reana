# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-job-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import docker

from invenio_db import db
from sqlalchemy_utils.types import UUIDType

from storm_compendium.compendium.records.models import CompendiumRecordMetadata
from storm_commons.records.base import BaseSQLAlchemyModel, BaseSQLAlchemyModelAPI

from invenio_records.systemfields import SystemFieldsMixin, ModelField
from storm_job_reana.config import DOCKER_REPOSITORY_PREFIX, DOCKER_IMAGE_PREFIX


class DockerImageCacheHandlerModel(db.Model, BaseSQLAlchemyModel):
    """Docker Image cache handler database model."""

    __tablename__ = "job_execution_image_cache"

    #
    # Related compendium
    #
    compendium = db.relationship(CompendiumRecordMetadata)
    compendium_id = db.Column(UUIDType, db.ForeignKey(CompendiumRecordMetadata.id))

    #
    # Associated Docker Image
    #
    service = db.Column(db.String, nullable=False)  # e.g., DockerHub, Quay.io

    image_name = db.Column(db.String, nullable=False)


class DockerImageCacheHandler(BaseSQLAlchemyModelAPI, SystemFieldsMixin):

    model_cls = DockerImageCacheHandlerModel
    """SQLAlchemy model class defining which table stores the records."""

    service = ModelField()

    compendium = ModelField()

    image_name = ModelField()


class DockerEnvironmentHandler:
    """Docker daemon handler."""

    @property
    def client(self):
        return self._client

    def __init__(self, client=None):
        self._client = client or docker.from_env()

    def build_image(self, nocache=True, rm=True, quiet=False, **kwargs):
        """Build an image."""
        return self._client.images.build(nocache=nocache, rm=rm, quiet=quiet, **kwargs)

    def push_image(self, repository, tag=None, **kwargs):
        """Push an image to a repository."""
        return self._client.images.push(repository, tag=tag, **kwargs)

    def remove_image(self, image, force=True, **kwargs):
        """Remove an image."""
        return self._client.images.remove(image, force=force, **kwargs)


class DockerImageIdentifierProvider:
    """Image unique identifier provider."""

    @staticmethod
    def generate(uuid_):
        """Generate a unique identifier for an Image."""

        # creating the image name
        image_name = DOCKER_IMAGE_PREFIX.format(uuid=str(uuid_))
        image_name = f"{DOCKER_REPOSITORY_PREFIX}/{image_name}:latest"

        return image_name


__all__ = "DockerHandler"
