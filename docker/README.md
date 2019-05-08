## Installation 

### Mac & Windows

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
### Build foglamp image

```
	docker build --tag foglamp --build-arg FOGLAMP_BRANCH=develop .
```

where name of the image is foglamp, FOGLAMP_BRANCH is the branch to build (develop, master, 1.5.2 ,etc)

### Run container


```
    $ docker run -d -v /foglamp-data:/usr/local/foglamp/data --name foglamp -p 8081:8081 -p 1995:1995 foglamp 
```

	-d : run foglamp container in detached mode
	-v : maps host volume foglamp-data to container volume /usr/local/foglamp/data
	--name : name of the container (foglamp)
	-p : map the port of host machine (8081) and container (:8081)
	foglamp : name of the image created in earlier step

> To attach to a running conatiner: `docker exec -it foglamp bash`


### Stopping docker container
```
    $ docker stop foglamp
```

> Note: The files in foglamp-data directory are created by container which creates/runs them as root user. In order to read the foglamp.db, you need to change the permission of foglamp.db* files, sudo chmod 666 foglamp.db* 