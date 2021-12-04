# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-reprozip is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Reprozip utility that allows you to run Docker unpackers inside Docker."""

import os

INCLUDE_USER_DEFINITION = os.getenv("INCLUDE_USER_DEFINITION", True)
