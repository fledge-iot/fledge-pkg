%define __spec_install_pre /bin/true
  
Name:          __NAME__
Vendor:        Dianomic Systems, Inc. <info@dianomic.com>
Version:       __VERSION__
Release:       1
BuildArch:     __ARCH__
Summary:       FogLAMP, the open source platform for the Internet of Things
License:       2019 Dianomic Systems Inc.
Group:         IOT
URL:           http://www.dianomic.com

%define install_path    /usr/local

Prefix:        /usr/local
Requires:      __REQUIRES__
AutoReqProv:   no


%description
__DESCRIPTION__

%pre

%preun
PKG_NAME="__PACKAGE_NAME__"


%post
set -e
set_files_ownership () {
	chown -R root:root /usr/local/foglamp/__INSTALL_DIR__
}

# main
echo "Setting ownership of FogLAMP files"
set_files_ownership


%files
