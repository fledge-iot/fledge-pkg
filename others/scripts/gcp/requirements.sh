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

# Jansson for encoding, decoding and manipulating JSON data
rm -rf jansson; git clone https://github.com/akheron/jansson.git
cd jansson
mkdir build
cd build
cmake ..
make
sudo make install
cd -

# libjwt which allows you to encode and decode JSON Web Tokens (JWT)
rm -rf libjwt; git clone https://github.com/benmcollins/libjwt.git
cd libjwt
autoreconf -i
./configure
make
sudo make install
