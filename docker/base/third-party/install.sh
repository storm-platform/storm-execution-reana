#!/bin/bash
#
# Copyright (C) 2021 Storm Project.
#
# storm-reprozip is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

for script in tools/*.sh; do
  chmod +x ${script}
  ./${script}
done
