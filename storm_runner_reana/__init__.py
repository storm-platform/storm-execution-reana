# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-runner-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Plugin for the Storm Runner to enable experiments execution on REANA instances."""

from .ext import StormRunnerReana
from .version import __version__


__all__ = ("__version__", "StormRunnerReana")
