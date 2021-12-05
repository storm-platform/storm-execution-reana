#
# Copyright (C) 2021 Storm Project.
#
# storm-reprozip is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

FROM golang:1.14.12

#
# Install base dependencies
#
RUN go get -u github.com/hugocarreira/go-decent-copy

#
# Build
#
COPY docker/parser/src/parser.go /usr/src/app/parser.go

WORKDIR /usr/src/app
RUN go build -o storm-parser parser.go
