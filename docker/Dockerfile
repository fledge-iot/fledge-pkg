FROM ubuntu:18.04

LABEL maintainer="info@dianomic.com"

ARG FLEDGE_BRANCH=develop
ENV FLEDGE_BRANCH ${FLEDGE_BRANCH}
RUN apt-get update && apt-get -y upgrade
# Ubuntu 20.04 LTS
# https://serverfault.com/questions/949991/how-to-install-tzdata-on-a-ubuntu-docker-image
# RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
RUN apt-get install -y git rsyslog sudo wget
# TODO: https://scaledb.atlassian.net/browse/FOGL-4809
# RUN apt-get install -y sqlite3

WORKDIR /fledge-core

RUN git clone -b $FLEDGE_BRANCH https://github.com/fledge-iot/fledge.git

RUN cd fledge && \
	chmod +x requirements.sh && \
	./requirements.sh && \
	make install

ENV FLEDGE_ROOT=/usr/local/fledge

VOLUME /usr/local/fledge/data

# These Volumes will be used in future when we want to install plugins
VOLUME /usr/local/fledge
VOLUME /fledge-core/fledge

EXPOSE 8081 1995 80


RUN wget -q -O - http://archives.fledge-iot.org/KEY.gpg | sudo apt-key add -
RUN echo "deb http://archives.fledge-iot.org/nightly/ubuntu1804/x86_64/ / " > /etc/apt/sources.list.d/fledge.list
RUN apt-get update

RUN sudo apt-get install -y nginx-light
RUN apt-get download fledge-gui && \
dpkg --unpack fledge-gui*.deb && \
sed -i 's/grep/echo/g' /var/lib/dpkg/info/fledge-gui.postinst && \
dpkg --configure fledge-gui

RUN echo "service rsyslog start" > start.sh && \
	echo "service nginx start" > start.sh && \
	echo "/usr/local/fledge/bin/fledge start" >> start.sh && \
	echo "tail -f /dev/null" >> start.sh && \
	chmod +x start.sh

CMD ["bash", "/fledge-core/start.sh"]
