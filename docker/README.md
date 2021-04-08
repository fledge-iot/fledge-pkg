## Installation 

### macOS & Windows

Install Docker CE for Mac and Windows (http://docker.com)

### Ubuntu

To install Docker CE follow the instructions given here:

https://docs.docker.com/engine/installation/linux/docker-ce/ubuntu/

### Red Hat Enterprise Linux (RHEL)

```
	sudo yum install yum-utils
	sudo yum-config-manager --enable rhui-REGION-rhel-server-extras
	sudo yum install docker
	sudo systemctl daemon-reload
	sudo systemctl restart docker
```
### Build fledge image

```
    $ docker build --tag fledge --build-arg FLEDGE_BRANCH=develop .
```

where name of the image is fledge, FLEDGE_BRANCH is the branch to build (develop, master, 1.5.2 ,etc)

### Run container


```
    $ docker run -d -v ~/fledge-data:/usr/local/fledge/data --name fledge -p 8081:8081 -p 1995:1995 fledge
```

	-d : run fledge container in detached mode
	-v : maps host volume /fledge-data to container volume /usr/local/fledge/data
	--name : name of the container (fledge)
	-p : map the port of host machine (8081) and container (:8081)
	fledge : name of the image created in earlier step

> To attach to a running conatiner: `docker exec -it fledge bash`

`--network host` mode makes the container use the host's network stack.

### Stopping docker container
```
    $ docker stop fledge
```

> Note: The files in fledge-data directory are created by container which creates/runs them as root user. In order to read the fledge.db, you need to change the permission of fledge.db* files, sudo chmod 666 fledge.db*

### notes...

docker save -o fledge-nightly.tar fledge:nightly


docker load < fledge-nightly.tar.gz
docker load --input fledge-nightly.tar.gz

docker run -d -v ~/fledge-data:/usr/local/fledge/data --name fledge -p 8081:8081 -p 1995:1995 -p 8082:80 fledge:nightly
docker run -d --name fledge -p 8081:8081 -p 1995:1995 -p 8082:80 fledge:nightly
