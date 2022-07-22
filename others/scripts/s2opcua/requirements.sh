#!/usr/bin/env bash

##---------------------------------------------------------------------------
## Copyright (c) 2022 Dianomic Systems Inc.
##
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
##
##     http://www.apache.org/licenses/LICENSE-2.0
##
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
##---------------------------------------------------------------------------

##
## Author: Ashish Jabble
##

set -e

os_name=`(grep -o '^NAME=.*' /etc/os-release | cut -f2 -d\" | sed 's/"//g')`
os_version=`(grep -o '^VERSION_ID=.*' /etc/os-release | cut -f2 -d\" | sed 's/"//g')`
echo "Platform is ${os_name}, Version: ${os_version}"

# mbedtls-dev:
if [[  $os_name == *"Red Hat"* || $os_name == *"CentOS"* ]]; then
    echo "RHEL/CentOS platform is not currently supported by this plugin."
    exit 1
else
    sudo apt-get install -y libmbedtls-dev
fi

# libexpat:
rm -rf libexpat
echo "Fetching an Expat, a C library for parsing XML..."
git clone https://github.com/libexpat/libexpat.git
(
	cd libexpat/expat
	./buildconf.sh && \
	./configure && \
	make && \
	sudo make install
)

# libcheck:
rm -rf check-0.15.2 check-0.15.2.tar.gz*
wget https://github.com/libcheck/check/releases/download/0.15.2/check-0.15.2.tar.gz
tar xf check-0.15.2.tar.gz
(
	cd check-0.15.2
	cp ../scripts/s2opcua/check-0.15.2_CMakeLists.txt.patch .
	patch < check-0.15.2_CMakeLists.txt.patch  # update the CMakeLists.txt file
	rm -f CMakeCache.txt
	mkdir -p build
	cd build
	cmake .. && make -j4 && sudo make install
)

# S2OPC:
rm -rf S2OPC
echo "Fetching S2OPC OPC UA Toolkit libraries..."
git clone https://gitlab.com/systerel/S2OPC.git
(
	cd S2OPC
	cp ../scripts/s2opcua/S2OPC.patch .
	git apply S2OPC.patch
	BUILD_SHARED_LIBS=OFF
	CMAKE_INSTALL_PREFIX=/usr/local
	./build.sh
	echo
	echo "BUILD done, INSTALLING..."
	echo
	cd build
	sudo make install
)
