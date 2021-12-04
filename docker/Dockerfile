# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Storm Project.
#
# storm-reprozip is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
FROM ubuntu:20.04

#
# Install base dependencies
#
RUN apt update -y \
    && apt install \
        python3 \
        python3-pip \
        python3-dev -y

#
# Install storm-reprozip
#
COPY . /opt/proxy/reprozip_proxy
RUN pip3 install /opt/proxy/reprozip_proxy

#
# Environment files
#
COPY docker/proxy.sh /proxy.sh
COPY docker/third-party/busybox /busybox
COPY docker/third-party/rpzsudo_x86-64_20210618-01 /rpzsudo

RUN chmod +x /busybox /rpzsudo /proxy.sh
