#!/bin/bash
#
# Copyright (C) 2021 Storm Project.
#
# storm-reprozip is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

#
# Download URL
#
RPZTAR_URL=https://github.com/remram44/rpztar/releases/download/v1/rpztar-x86_64

#
# Download the rpztar (x86-64)
#
wget -O /rpztar ${RPZTAR_URL}
