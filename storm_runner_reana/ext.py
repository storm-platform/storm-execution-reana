# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-runner-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

import storm_runner_reana.config as config
from storm_runner_reana.contrib.plugin import init_plugins


class StormRunnerReana:
    """Flask extension for the Storm Runner Reana services plugin."""

    def __init__(self, app=None):
        """Plugin initialization."""
        if app:
            self.init_app(app)

    def init_app(self, app):
        """Flask application initialization."""
        self.init_config(app)
        self.init_plugin_services(app)

        app.extensions["storm-runner-reana"] = self

    def init_config(self, app):
        """Initialize the application config."""
        for k in dir(config):
            if k.startswith("STORM_RUNNER_REANA_"):
                app.config.setdefault(k, getattr(config, k))

    def init_plugin_services(self, app):
        """Initialize the plugin services."""
        self.plugin_services = init_plugins()


__all__ = "StormRunnerReana"
