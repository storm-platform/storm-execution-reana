# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-job-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_job_reana.modules.reprozip.service import job_service


def job_service_metadata():
    """Reana-Reprozip service metadata."""
    return {
        "id": "reana-reprozip",
        "metadata": {
            "title": "Reana-Reprozip Job executor",
            "description": "Job executor for running pipelines created with Reprozip using the Reana platform.",
            "supported_descriptors": ["storm-core>=1.0,<2"],
        },
        "service": job_service,
    }


__all__ = "job_service_metadata"
