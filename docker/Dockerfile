FROM ubuntu:18.04

MAINTAINER Vaibhav Singhal "vaibhav@dianomic.com"

ARG FOGLAMP_BRANCH=master
ENV FOGLAMP_BRANCH ${FOGLAMP_BRANCH}
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y git rsyslog

WORKDIR /foglamp-core

RUN git clone --single-branch -b $FOGLAMP_BRANCH https://github.com/foglamp/FogLAMP.git 

RUN cd FogLAMP && \
	sed -i 's/sudo//g' requirements.sh && \
	sh requirements.sh && \
	make install

RUN echo "service rsyslog start" > start.sh && \
	echo "/usr/local/foglamp/bin/foglamp start" >> start.sh && \
	echo "tail -f /dev/null" >> start.sh && \
	chmod +x start.sh
	

ENV FOGLAMP_ROOT=/usr/local/foglamp

VOLUME /usr/local/foglamp/data
VOLUME /usr/local/foglamp
VOLUME /foglamp-core/FogLAMP

EXPOSE 8081 1995

CMD ["bash", "/foglamp-core/start.sh"]

