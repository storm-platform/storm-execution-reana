#!/bin/bash
#
# Copyright (C) 2021 Storm Project.
#
# storm-reprozip is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

#
# Download URL
#
RPZSUDO_URL=https://github.com/remram44/static-sudo/releases/download/current/rpzsudo-x86_64

#
# Download the rpzsudo (x86-64)
#
wget -O /rpzsudo ${RPZSUDO_URL}
