# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# reprozip-proxy is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Reprozip utility that allows you to run Docker unpackers inside Docker."""

import os

PROXY_DATA = os.getenv("PROXY_DATA", "/proxy")
