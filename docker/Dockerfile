FROM ubuntu:18.04

MAINTAINER Vaibhav Singhal "vaibhav@dianomic.com"

ARG FLEDGE_BRANCH=main
ENV FLEDGE_BRANCH ${FLEDGE_BRANCH}
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y git rsyslog

WORKDIR /fledge-core

RUN git clone --single-branch -b $FLEDGE_BRANCH https://github.com/fledge-iot/fledge.git

RUN cd fledge && \
	chmod +x requirements.sh && \
	./requirements.sh && \
	make install

RUN echo "service rsyslog start" > start.sh && \
	echo "/usr/local/fledge/bin/fledge start" >> start.sh && \
	echo "tail -f /dev/null" >> start.sh && \
	chmod +x start.sh
	

ENV FLEDGE_ROOT=/usr/local/fledge

VOLUME /usr/local/fledge/data

# These Volumes will be used in future when we want to install plugins
VOLUME /usr/local/fledge
VOLUME /fledge-core/fledge

EXPOSE 8081 1995

CMD ["bash", "/fledge-core/start.sh"]

