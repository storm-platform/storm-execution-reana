#
# Copyright (C) 2021 Storm Project.
#
# storm-reprozip is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

FROM amd64/busybox:1.30.0-glibc as busybox
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
# Install busybox (1.30 glibc - used to fix bug 11651[https://bugs.busybox.net/show_bug.cgi?id=11651])
#
COPY --from=busybox /bin/busybox /busybox
RUN ["/busybox", "--install", "/bin"]

#
# Install storm-reprozip
#
COPY . /opt/proxy/reprozip_proxy
RUN pip3 install /opt/proxy/reprozip_proxy

#
# Environment files
#


COPY docker/proxy.sh /proxy.sh
COPY docker/third-party/rpztar /rpztar
COPY docker/third-party/rpzsudo_x86-64_20210618-01 /rpzsudo

RUN chmod +x /busybox /rpzsudo /rpztar /proxy.sh
