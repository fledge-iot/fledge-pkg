%define __spec_install_pre /bin/true
  
Name:          __NAME__
Vendor:        Dianomic Systems, Inc. <info@dianomic.com>
Version:       __VERSION__
Release:       __RELEASE__
BuildArch:     __ARCH__
Summary:       Fledge __NAME__ plugin, the open source platform for the Internet of Things
License:       Apache License
Group:         IOT
URL:           http://www.dianomic.com
VCS:           __VCS__

%define install_path    /usr/local

Prefix:        /usr/local
Requires:      __REQUIRES__
AutoReqProv:   no


%description
__DESCRIPTION__

%pre
#!/usr/bin/env bash

##--------------------------------------------------------------------
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
##--------------------------------------------------------------------

##--------------------------------------------------------------------
##
## This script is used to execute pre installation tasks.
##
## Author: Mark Riddoch
##
##--------------------------------------------------------------------



%preun
#!/usr/bin/env bash

##--------------------------------------------------------------------
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
##--------------------------------------------------------------------

##--------------------------------------------------------------------
##
## This script is used to execute before the removal of files associated with the package.
##
## Author: Ivan Zoratti, Ashwin Gopalakrishnan, Stefano Simonelli
##
##----------------------------------------------------------------------------------------

# FIXME_I
#set -e

PKG_NAME="__PACKAGE_NAME__"


%post
#!/usr/bin/env bash

##--------------------------------------------------------------------
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
##--------------------------------------------------------------------

##--------------------------------------------------------------------
##
## This script is used to execute post installation tasks.
##
## Author: Ivan Zoratti, Massimiliano Pinto, Stefano Simonelli
##
##--------------------------------------------------------------------

set -e



set_files_ownership () {
	chown -R root:root /usr/local/fledge/__INSTALL_DIR__
}

# main
echo "Setting ownership of Fledge files"
set_files_ownership

# Install Prerequisite; if any
if [ -f /usr/local/fledge/python/extras_install___PLUGIN_NAME__.sh ]; then
   sh /usr/local/fledge/python/extras_install___PLUGIN_NAME__.sh
fi

# Install any Python dependencies
if [ -f /usr/local/fledge/__INSTALL_DIR__/requirements.txt ]; then
	bash << EOF
scl enable rh-python36 bash
pip install -Ir /usr/local/fledge/__INSTALL_DIR__/requirements.txt
EOF
fi

echo __PLUGIN_NAME__ __PLUGIN_TYPE__ plugin is installed.

%files
