# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-job-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from functools import wraps

from storm_job.job.models.api import ExecutionJob
from storm_pipeline.pipeline.records.api import ResearchPipeline


def pass_records(f):
    """Decorator to load the ExecutionJob and ResearchPipeline."""

    @wraps(f)
    def wrapper(job_id, reana_access_token, *args, **kwargs):
        try:

            # loading the defined deposit record
            job_object = ExecutionJob.get_record(id=job_id)
            pipeline_object = ResearchPipeline.pid.resolve(
                job_object.pipeline.data.get("id")
            )

        except:
            raise RuntimeError("Is not possible to load the Job and Pipeline records.")

        return f(
            job=job_object,
            pipeline=pipeline_object,
            reana_access_token=reana_access_token,
            *args,
            **kwargs
        )

    return wrapper
