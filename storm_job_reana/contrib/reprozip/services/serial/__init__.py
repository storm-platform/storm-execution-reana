# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-job-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

from storm_job_reana.contrib.reprozip.services.serial.tasks import service_task


class PluginService:

    #
    # General definitions
    #
    id = "job-reprozip-serial"

    #
    # Service task
    #
    service = service_task

    #
    # General plugin service description
    #
    metadata = {
        "title": "Reana-Reprozip job plugin (Serial execution mode)",
        "description": "Job plugin to execute reprozip experiments with Reana services using the serial mode.",
        "supported_descriptors": ["storm-core>=1.0,<2"],
        "required_fields": [
            {
                "title": "REANA Rest API Access Token",
                "description": "Your REANA access token, used to connect to preparing the Execution Job in the REANA.",
                "field_name": "reana_access_token",
            }
        ],
    }

    #
    # Extra fields availables
    #
    extras = {}
