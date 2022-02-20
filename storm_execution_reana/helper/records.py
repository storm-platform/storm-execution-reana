# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-execution-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from functools import wraps

from storm_execution.execution.models.api import ExecutionTask
from storm_pipeline.pipeline.records.api import ResearchPipeline


def pass_records(f):
    """Decorator to load the ExecutionTask and ResearchPipeline."""

    @wraps(f)
    def wrapper(execution_id, reana_access_token, *args, **kwargs):
        try:

            # loading the defined deposit record
            execution_object = ExecutionTask.get_record(id=execution_id)
            pipeline_object = ResearchPipeline.pid.resolve(
                execution_object.pipeline.data.get("id")
            )

        except:
            raise RuntimeError(
                "Is not possible to load the Execution Tasks and Pipeline records."
            )

        return f(
            execution=execution_object,
            pipeline=pipeline_object,
            reana_access_token=reana_access_token,
            *args,
            **kwargs
        )

    return wrapper
