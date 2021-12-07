#
# Copyright (C) 2021 Storm Project.
#
# storm-job-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

#
# Compiled tool layers
#
FROM amd64/busybox:1.30.0-glibc as busybox
FROM storm/storm-reprozip-parser:0.1 as storm-parser

FROM ubuntu:20.04

#
# Install base dependencies
#
RUN apt update -y \
    && apt install \
        git \
        python3 \
        python3-pip \
        python3-dev -y

#
# Install busybox (1.30 glibc - used to fix bug 11651[https://bugs.busybox.net/show_bug.cgi?id=11651])
#
COPY --from=busybox /bin/busybox /busybox
RUN ["/busybox", "--install", "/bin"]

#
# Install storm-reprozip-parser
#
COPY --from=storm-parser /usr/src/app/storm-parser /storm-parser

#
# Install storm-reprozip
#
COPY . /opt/proxy/reprozip_proxy
RUN cd /opt/proxy/reprozip_proxy/ \
    && pip3 install -e .[reprozip-cli]

#
# Environment files
#
COPY docker/reprozip/base/third-party/ /opt/third-party
RUN cd /opt/third-party \
    && chmod +x install.sh \
    && ./install.sh

RUN chmod +x /rpzsudo /rpztar /storm-parser
