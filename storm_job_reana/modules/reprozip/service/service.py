# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-job-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.


from storm_job_reana.modules.reprozip.service.strategy import WorkflowSchedulerStrategy


def job_service(pipeline_id: str, **kwargs):
    """Storm Job Reana service.

    Args:
        pipeline_id (str): Pipeline that will be processed.

        kwargs (dict): Extra arguments for the execution strategy.
    """

    # Select the execution strategy.
    workflow_scheduler_type = kwargs.get("type")
    strategy_fnc = WorkflowSchedulerStrategy.get_strategy(workflow_scheduler_type)

    # Apply the strategy
    return strategy_fnc.delay(pipeline_id, **kwargs)


__all__ = "job_service"
