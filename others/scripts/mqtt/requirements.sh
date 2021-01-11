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

git clone https://github.com/eclipse/paho.mqtt.c.git
sudo apt-get install libssl-dev pkg-config
cd paho.mqtt.c
mkdir build
cd build
cmake -DPAHO_BUILD_DOCUMENTATION=FALSE -DPAHO_WITH_SSL=TRUE ..
make
sudo make install
