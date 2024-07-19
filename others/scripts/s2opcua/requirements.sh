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

os_name=$(grep -o '^NAME=.*' /etc/os-release | cut -f2 -d\" | sed 's/"//g')
os_version=$(grep -o '^VERSION_ID=.*' /etc/os-release | cut -f2 -d\" | sed 's/"//g')
echo "Platform is ${os_name}, Version: ${os_version}"
git_root=$(pwd)

# mbedtls-dev:
cd ${git_root}
mbetls_version='2.28.7'
if [[  $os_name == *"Red Hat"* || $os_name == *"CentOS"* ]]; then
    echo "RHEL/CentOS platform is not currently supported by this plugin."
    exit 1
else
    rm -rf v${mbetls_version}.tar.gz mbedtls-${mbetls_version}
    wget "https://github.com/Mbed-TLS/mbedtls/archive/v${mbetls_version}.tar.gz"
    tar xzvf v${mbetls_version}.tar.gz
    cd mbedtls-${mbetls_version}
    mkdir build
    cd build
    cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_POSITION_INDEPENDENT_CODE=ON -DUSE_SHARED_MBEDTLS_LIBRARY=OFF ..
    make
    sudo make install
fi

# libexpat:
cd ${git_root}
libexpat_version="2.6.0"
libexpat_branch="R_${libexpat_version//./_}"
rm -rf libexpat
git clone https://github.com/libexpat/libexpat.git --branch ${libexpat_branch} --depth 1
(
	cd libexpat/expat
	./buildconf.sh && \
	./configure && \
	make && \
	sudo make install
)

# libcheck:
cd ${git_root}
lib_check_version="0.15.2"
rm -rf check-${lib_check_version}.tar.gz check-${lib_check_version}
wget https://github.com/libcheck/check/releases/download/${lib_check_version}/check-${lib_check_version}.tar.gz
tar xf check-${lib_check_version}.tar.gz
(
	cd check-${lib_check_version}
	cp ${git_root}/scripts/s2opcua/check-${lib_check_version}_CMakeLists.txt.patch .
	patch < check-${lib_check_version}_CMakeLists.txt.patch  # update the CMakeLists.txt file
	rm -f CMakeCache.txt
	mkdir -p build
	cd build
	cmake .. && make -j4 && sudo make install
)

# S2OPC
cd ${git_root}
s2opc_toolkit_version="1.5.0"
rm -rf S2OPC
git clone https://gitlab.com/systerel/S2OPC.git --branch S2OPC_Toolkit_${s2opc_toolkit_version} --depth 1
(
	cd S2OPC
	BUILD_SHARED_LIBS=1 CMAKE_INSTALL_PREFIX=/usr/local ./build.sh
	echo
	echo "BUILD done, INSTALLING..."
	echo
	cd build
	sudo make install
	sudo cp ../src/ClientServer/frontend/client_wrapper/libs2opc_client_config_custom.h /usr/local/include/s2opc/clientserver
)

