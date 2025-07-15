### Build Fledge image

```
    $ docker build --no-cache --tag fledge:latest-ubuntu2004 -f Dockerfile .
```

Default will be built with the latest stable release.

```
    $ docker build --tag fledge:nightly-ubuntu2004-aarch64 --build-arg version=20.04 --build-arg arch=aarch64 --build-arg package_version=nightly --build-arg packages="fledge-south-lathe fledge-south-sinusoid fledge-north-http-north" -f Dockerfile .
```

The image is referred to as fledge, and it is tagged as nightly-ubuntu2004-aarch64. The package_version denotes the version of the packages, such as latest, nightly, fixes/FOGL-XXXX.

##### Build Arguments:

a) **version** - The name of the Ubuntu version is either 18.04 or 20.04. By default, the version is 20.04.

b) **arch** - The Ubuntu architecture is designated as either x86_64 or aarch64. The default architecture is x86_64.

c) **package_version** - The package version can be either the latest, nightly, or fixes/FOGL-XXXX. By default, it is set to nightly.

d) **packages** - A compilation of packages delineated by spaces. For instance, packages="fledge-south-lathesim fledge-south-sinusoid fledge-north-http-north".

e) **USERNAME** - Name of the non-root user. By default, it is fledge.


### Run container


```
    $ docker run -d --name fledge -p 8081:8081 -p 1995:1995 -p 8082:80 fledge:nightly-ubuntu2004-aarch64
```

	-d : run fledge container in detached mode
	-p : map the ports, e.g host machine (8081) to container (:8081)


To attach to a running container: `docker exec -it fledge bash`


