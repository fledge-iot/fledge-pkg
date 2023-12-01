#!/usr/bin/env bash

##--------------------------------------------------------------------
## Copyright (c) 2021 Dianomic Systems
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
##--------------------------------------------------------------------

##
## Author: Ashish Jabble
##

set -e
os_name=`(grep -o '^NAME=.*' /etc/os-release | cut -f2 -d\" | sed 's/"//g')`
os_version=`(grep -o '^VERSION_ID=.*' /etc/os-release | cut -f2 -d\" | sed 's/"//g')`
echo "Platform is ${os_name}, Version: ${os_version}"

if [[ ( $os_name == *"Red Hat"* || $os_name == *"CentOS"* ) &&  $os_version == *"7"* ]]; then
    if [[ $os_name == *"Red Hat"* ]]; then
        sudo yum-config-manager --enable 'Red Hat Enterprise Linux Server 7 RHSCL (RPMs)'
        sudo yum install -y @development
    else
        sudo yum groupinstall "Development tools" -y
        sudo yum install -y centos-release-scl
    fi
    sudo yum install -y openssl-devel

    # A gcc version newer than 4.9.0 is needed to properly use <regex>
    # the installation of these packages will not overwrite the previous compiler
    # the new one will be available using the command 'source scl_source enable devtoolset-7'
    # the previous gcc will be enabled again after a log-off/log-in.
    #
    sudo yum install -y yum-utils
    sudo yum-config-manager --enable rhel-server-rhscl-7-rpms
    sudo yum install -y devtoolset-7
elif apt --version 2>/dev/null; then
	  sudo apt install -y libssl-dev pkg-config
else
	  echo "Requirements are not supported for platform: ${os_name} and having version: ${os_version}"
fi
rm -rf paho.mqtt.c
git clone --depth 1 --branch v1.3.13 https://github.com/eclipse/paho.mqtt.c.git
cd paho.mqtt.c
mkdir build
cd build
cmake -DPAHO_BUILD_DOCUMENTATION=FALSE -DPAHO_WITH_SSL=TRUE ..
make
sudo make install

cd ..
cd ..

rm -rf paho.mqtt.cpp
git clone --depth 1 --branch v1.3.1 https://github.com/eclipse/paho.mqtt.cpp
cd paho.mqtt.cpp
cp ../scripts/mqtt/paho-mqtt-cpp.patch .
git apply paho-mqtt-cpp.patch
cmake -Bbuild -H. -DPAHO_BUILD_STATIC=ON -DPAHO_WITH_SSL=ON -DPAHO_BUILD_DOCUMENTATION=FALSE -DPAHO_BUILD_SAMPLES=FALSE
sudo cmake --build build/ --target install
sudo ldconfig
cd ..

