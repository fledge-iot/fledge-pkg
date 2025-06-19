ARG arch=x86_64
ARG version=20.04
FROM --platform=linux/${arch} ubuntu:${version}

LABEL maintainer="info@dianomic.com"
LABEL org.opencontainers.image.title="Fledge IIoT Platform"
LABEL org.opencontainers.image.description="Fledge IIoT platform featuring secure execution for a non-root fledge user."

# Define build-time arguments
ARG arch
ARG version
ARG package_version=nightly
ARG default_packages="fledge fledge-gui"
ARG packages=""
ARG USERNAME=fledge
ARG UID=1001
ARG GID=1001

# Define environment variables
ENV FLEDGE_ROOT=/usr/local/fledge \
    SYSLOG_UDP_ENABLED=True

# Set shell to bash for script compatibility
SHELL ["/bin/bash", "-c"]

# Copy setup scripts
COPY setup.sh nginx.conf /tmp/

# fledge packages setup
RUN set -e && \
    os_version="ubuntu${version//./}" && \
    # Append user-supplied packages to default packages
    if [[ -n "${packages}" ]]; then \
        all_packages="${default_packages} ${packages}"; \
    else \
        all_packages="${default_packages}"; \
    fi && \
    /tmp/setup.sh "${USERNAME}" \
                  "http://archives.fledge-iot.org/${package_version}/${os_version}/${arch}/" \
                  "${UID}" "${GID}" "${all_packages}" && \
    rm -f /tmp/setup.sh

# Set user context and working directory
USER ${UID}:${GID}
WORKDIR /home/${USERNAME}

# Expose Fledge ports
EXPOSE 8081 1995 8080 5140

# Default command
CMD ["bash", "start.sh"]
