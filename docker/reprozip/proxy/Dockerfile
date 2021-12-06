#
# Copyright (C) 2021 Storm Project.
#
# storm-job-reana is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

FROM storm/storm-reprozip-base:0.1

#
# Environment variable
#
ENV REPROZIP_INCLUDE_USER_DEFINITION=0

#
# Copy files
#
COPY docker/reprozip/proxy/tools/proxy.sh /proxy.sh

#
# Configure container execution
#
CMD ["/proxy.sh"]
