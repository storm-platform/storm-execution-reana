FROM {{proxy_image}}

#
# Copying files
#
COPY {{bundle_file}} /opt/input/package.rpz

#
# Proxing!
#
RUN /proxy.sh
