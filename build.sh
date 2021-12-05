#!/bin/bash
#
# Copyright (C) 2021 Storm Project.
#
# storm-reprozip is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

REPOSITORY_TAG=0.1

#
# Build dependencies
#
docker build -t "storm/storm-reprozip-parser:${REPOSITORY_TAG}" -f docker/parser/Dockerfile .

#
# Base environment
#
docker build -t "storm/storm-reprozip-base:${REPOSITORY_TAG}" -f docker/base/Dockerfile .

#
# Proxy tool
#
docker build -t "storm/storm-reprozip-proxy:${REPOSITORY_TAG}" -f docker/proxy/Dockerfile .
