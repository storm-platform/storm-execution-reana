# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-execution-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from functools import wraps

from storm_execution.execution.models.api import ExecutionTask
from storm_workflow.workflow.records.api import ResearchWorkflow


def pass_records(f):
    """Decorator to load the ExecutionTask and ResearchWorkflow."""

    @wraps(f)
    def wrapper(execution_id, reana_access_token, *args, **kwargs):
        try:

            # loading the defined deposit record
            execution_object = ExecutionTask.get_record(id=execution_id)
            workflow_object = ResearchWorkflow.pid.resolve(
                execution_object.workflow.data.get("id")
            )

        except:
            raise RuntimeError(
                "Is not possible to load the Execution Tasks and Pipeline records."
            )

        return f(
            execution=execution_object,
            workflow=workflow_object,
            reana_access_token=reana_access_token,
            *args,
            **kwargs
        )

    return wrapper
