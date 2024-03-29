### Build fledge Ubuntu 18.04 image

```
    $ docker build --no-cache --tag fledge:latest -f Dockerfile.ubuntu1804 .
```

Default image will be built with latest stable relase.

```
    $ docker build --tag fledge:nightly --build-arg PKG_VERSION=nightly -f Dockerfile.ubuntu1804 .
```


 name of the image is fledge and tag nightly, PKG_VERSION is the version of packages (latest, nightly etc.)


### Run container


```
    $ docker run -d -v ~/fledge-data:/usr/local/fledge/data --name fledge -p 8081:8081 -p 1995:1995 -p 8082:80 fledge:latest
```

	-d : run fledge container in detached mode
	-v : maps host volume /fledge-data to container volume /usr/local/fledge/data
	--name : name of the container (fledge)
	-p : map the port of host machine (8081) and container (:8081)
	fledge : name of the image created in earlier step, with tag latest

> To attach to a running conatiner: `docker exec -it fledge bash`

`--network host` mode makes the container use the host's network stack.

# Tag and push to registry

  $ sudo docker tag fledge:latest 100.25.163.15:5000/fledge:latest
  
  $ sudo docker push 100.25.163.15:5000/fledge:latest
