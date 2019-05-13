%define __spec_install_pre /bin/true
  
Name:          __NAME__
Vendor:        Dianomic Systems, Inc. <info@dianomic.com>
Version:       __VERSION__
Release:       1
BuildArch:     __ARCH__
Summary:       FogLAMP, the open source platform for the Internet of Things
License:       Apache License
Group:         IOT
URL:           http://www.dianomic.com

%define install_path    /usr/local

Prefix:        /usr/local
Requires:      __REQUIRES__
AutoReqProv:   no


%description
__DESCRIPTION__

%pre
#!/usr/bin/env bash

##--------------------------------------------------------------------
## Copyright (c) 2019 Dianomic Systems Inc.
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
## Copyright (c) 2019 Dianomic Systems Inc.
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
## Copyright (c) 2019 Dianomic Systems Inc.
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
	chown -R root:root /usr/local/foglamp/__INSTALL_DIR__
}

# main
echo "Setting ownership of FogLAMP files"
set_files_ownership


%files
