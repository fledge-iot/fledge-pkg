%define __spec_install_pre /bin/true

Name:          __NAME__
Vendor:        Dianomic Systems, Inc. <info@dianomic.com>
Version:       __VERSION__
Release:       __RELEASE__
BuildArch:     __ARCH__
Summary:       Fledge, the open source platform for the Internet of Things
License:       Apache License
Group: 	       IoT
Packager:      Dianomic Systems, Inc.
URL:           http://www.dianomic.com
VCS:           __VCS__

%define install_path	/usr/local

Prefix:        /usr/local
Requires:      dbus-devel, glib2-devel, boost, openssl, rh-python36, yum-utils, gcc, autoconf, curl, libtool,  rsyslog,  wget, zlib, libuuid, avahi, sudo, krb5-workstation, curl-devel, python3-numpy
AutoReqProv:   no

%description
Fledge, the open source platform for the Internet of Things


## -------------------------------------------------------------------------------------------------
## Scriptlet values which we must use in our scripts

## scriptlet     install          upgrade          uninstall
## %pre          $1 == 1          $1 == 2          (N/A)
## %post         $1 == 1          $1 == 2          (N/A)
## %preun        (N/A)            $1 == 1          $1 == 0
## %postun       (N/A)            $1 == 1          $1 == 0


## On upgrade, the scripts are run in the following order:

## %pre of new package
## %post of new package
## %preun of old package
## %postun of old package

## --------------------------------------------------------------------------------------------------

%pre
#!/usr/bin/env bash

##---------------------------------------------------------------------------------------------------
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
##---------------------------------------------------------------------------------------------------

##---------------------------------------------------------------------------------------------------
##
## The %pre scriptlet executes just before the package is to be installed.
##
## Author: Ivan Zoratti, Ashwin Gopalakrishnan, Massimiliano Pinto, Stefano Simonelli, Ashish Jabble
##
##---------------------------------------------------------------------------------------------------

set -e

PKG_NAME="fledge"

is_fledge_installed () {
	set +e
    rc=$(rpm -ql ${PKG_NAME} | grep 'fledge/bin/fledge$')
    echo $rc
    set -e
}

get_fledge_script () {
    fledge_script=$(rpm -ql ${PKG_NAME} | grep 'fledge/bin/fledge$')
    echo $fledge_script
}

is_fledge_running () {
    set +e
    fledge_script=$(get_fledge_script)
    fledge_status_output=$($fledge_script status 2>&1 | grep 'Fledge Uptime')
    rc=$((!$?))
    echo $rc
    set -e
}

get_current_version_file () {
    current_version_file=$(rpm -ql ${PKG_NAME} | grep VERSION)
    echo $current_version_file
}

get_schema_version () {
    version_file=$1
    schema_version=$(grep fledge_schema $version_file | awk -F = '{print $2}')
    echo $schema_version
}

exists_schema_change_path () {
    echo 1
}

stop_fledge_service () {
    systemctl stop fledge
}

kill_fledge () {
    set +e
    fledge_script=$(get_fledge_script)
    fledge_status_output=$($fledge_script kill 2>&1)
    set -e
}

disable_fledge_service () {
	set +e
	/sbin/chkconfig fledge off
    set -e
}

remove_fledge_service_file () {
    rm -rf /etc/init.d/fledge
}

reset_systemctl () {
    systemctl daemon-reload
    systemctl reset-failed
}

# main
if [ $1 == 1 ];then
    echo "pre scriptlet is called: ${PKG_NAME} is getting installed."
    # Add steps here for the fresh installed case for this scriptlet
elif [ $1 == 2 ];then
    echo "pre scriptlet is called: ${PKG_NAME} is getting upgraded."
    IS_FLEDGE_RUNNING=$(is_fledge_running)
    if [ "$IS_FLEDGE_RUNNING" -eq "1" ]
    then
        echo "${PKG_NAME} is currently running."
        echo "Stop ${PKG_NAME} service."
        stop_fledge_service
        echo "Kill ${PKG_NAME}."
        kill_fledge
    fi

    echo "Disable ${PKG_NAME} service."
    disable_fledge_service
    echo "Remove ${PKG_NAME} service script"
    remove_fledge_service_file
    echo "Reset systemctl"
    reset_systemctl

    # Persist current version in case of upgrade/downgrade
    installed_version=`rpm -qi ${PKG_NAME} | grep Version |awk '{print $3}'`
    if [ "${installed_version}" ]
    then
        # Persist current ${PKG_NAME} version: it will be removed by postinstall script
        this_dir=`pwd`
        cd /usr/local/fledge/
        echo "${installed_version}" > .current_installed_version
        cd ${this_dir}
    fi

    # check schema version file, exit if schema change path does not exist
    CURRENT_VERSION_FILE=$(get_current_version_file)
    CURRENT_SCHEMA_VERSION=$(get_schema_version $CURRENT_VERSION_FILE)
    echo "${PKG_NAME} currently has schema version $CURRENT_SCHEMA_VERSION"
    EXISTS_SCHEMA_CHANGE_PATH=$(exists_schema_change_path)
    if [ "$EXISTS_SCHEMA_CHANGE_PATH" -eq "0" ]
    then
        echo "*** ERROR. There is no schema change path from the installed version to the new version. ***"
        exit 1
    fi
fi


%preun
#!/usr/bin/env bash

##--------------------------------------------------------------------------------
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
##--------------------------------------------------------------------------------

##--------------------------------------------------------------------------------
##
## The %preun scriptlet executes just before the package is to be erased.
##
## Author: Ivan Zoratti, Ashwin Gopalakrishnan, Stefano Simonelli, Ashish Jabble
##
##--------------------------------------------------------------------------------

set -e

PKG_NAME="fledge"

get_fledge_script () {
    fledge_script=$(rpm -ql ${PKG_NAME} | grep 'fledge/bin/fledge$')
    echo $fledge_script
}

stop_fledge_service () {
    systemctl stop fledge
}

is_fledge_running () {
    set +e
    fledge_script=$(get_fledge_script)
    fledge_status_output=$($fledge_script status 2>&1 | grep 'Fledge Uptime')
    rc=$((!$?))
    echo $rc
    set -e
}

kill_fledge () {
    set +e
    fledge_script=$(get_fledge_script)
    fledge_status_output=$($fledge_script kill 2>&1)
    set -e
}

disable_fledge_service () {
	set +e
	/sbin/chkconfig fledge off
    set -e
}

remove_fledge_service_file () {
    rm -rf /etc/init.d/fledge
}

reset_systemctl () {
    systemctl daemon-reload
    systemctl reset-failed
}

# main
if [ $1 == 1 ];then
    echo "preun scriptlet is called: ${PKG_NAME} is getting upgraded."
elif [ $1 == 0 ];then
    echo "preun scriptlet is called: ${PKG_NAME} is getting removed/uninstalled."
    IS_FLEDGE_RUNNING=$(is_fledge_running)
    if [ "$IS_FLEDGE_RUNNING" -eq "1" ]
    then
        echo "${PKG_NAME} is currently running."
        echo "Stop ${PKG_NAME} service."
        stop_fledge_service
        echo "Kill ${PKG_NAME}."
        kill_fledge
    fi

    echo "Disable ${PKG_NAME} service."
    disable_fledge_service
    echo "Remove ${PKG_NAME} service script"
    remove_fledge_service_file
    echo "Reset systemctl"
    reset_systemctl
fi


%post
#!/usr/bin/env bash

##----------------------------------------------------------------------------
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
##----------------------------------------------------------------------------

##----------------------------------------------------------------------------
##
## The %post scriptlet executes just after the package is to be installed.
##
## Author: Ivan Zoratti, Massimiliano Pinto, Stefano Simonelli, Ashish Jabble
##
##----------------------------------------------------------------------------

set -e

# certificate generation defaults
SSL_NAME="fledge"
SSL_DAYS="365"
AUTH_NAME="ca"

link_update_task() {
    echo "Changing setuid of update_task.yum"
    chmod ugo+s /usr/local/fledge/bin/update_task.yum
    echo "Removing task/update"
    [ -e /usr/local/fledge/scripts/tasks/update ] && rm  /usr/local/fledge/scripts/tasks/update
    echo "Create link file"
    ln -s /usr/local/fledge/bin/update_task.yum /usr/local/fledge/scripts/tasks/update
}

copy_fledge_sudoer_file() {
    cp /usr/local/fledge/bin/fledge.sudoers_rh /etc/sudoers.d/fledge
}

copy_service_file() {
    cp /usr/local/fledge/extras/scripts/fledge.service /etc/init.d/fledge
}

enable_fledge_service() {
	/sbin/chkconfig fledge on
}

start_fledge_service() {
    systemctl start fledge
}

set_files_ownership () {
    chown root:root /etc/init.d/fledge
    chown -R root:root /usr/local/fledge
    chown -R ${SUDO_USER}:${SUDO_USER} /usr/local/fledge/data

}

generate_certs () {
    if [ ! -f /usr/local/fledge/data/etc/certs/fledge.cert ]; then
        echo "Certificate files do not exist. Generating new certificate files."
        cd /usr/local/fledge
        ./scripts/certificates ${SSL_NAME} ${SSL_DAYS}
    else
        echo "Certificate files already exist. Skipping generating new certificate files."
    fi
}

generate_auth_certs () {
    if [ ! -f /usr/local/fledge/data/etc/certs/ca.cert ]; then
        echo "CA Certificate file does not exist. Generating new CA certificate file."
        cd /usr/local/fledge
        ./scripts/auth_certificates ca ${AUTH_NAME} ${SSL_DAYS}
    else
        echo "CA Certificate file already exists. Skipping generating new CA certificate file."
    fi
    if [ ! -f /usr/local/fledge/data/etc/certs/admin.cert ]; then
        echo "Admin Certificate file does not exist. Generating new admin certificate file."
        cd /usr/local/fledge
        ./scripts/auth_certificates user admin ${SSL_DAYS}
    else
        echo "Admin Certificate file already exists. Skipping generating new admin certificate file."
    fi
    if [ ! -f /usr/local/fledge/data/etc/certs/user.cert ]; then
        echo "User Certificate file does not exist. Generating new user certificate file."
        cd /usr/local/fledge
        ./scripts/auth_certificates user user ${SSL_DAYS}
    else
        echo "User Certificate file already exists. Skipping generating new user certificate file."
    fi
}

copy_new_data () {
    if [ ! -d /usr/local/fledge/data ]; then
        echo "Data directory does not exist. Using new data directory"
        mv /usr/local/fledge/data.new /usr/local/fledge/data
    else
        echo "Data directory already exists. Updating data/extras/fogbench/fogbench_sensor_coap.template.json only."
        if [ -f /usr/local/fledge/data.new/extras/fogbench/fogbench_sensor_coap.template.json  ]; then

            cp /usr/local/fledge/data.new/extras/fogbench/fogbench_sensor_coap.template.json /usr/local/fledge/data/extras/fogbench/fogbench_sensor_coap.template.json
		fi
        rm -rf /usr/local/fledge/data.new
    fi
}

install_pip3_packages () {
	set +e

	foglam_test="added by Fledge"
	check_already_added=`cat /home/${SUDO_USER}/.bashrc | grep -c "${foglam_test}"`

	if [ "$check_already_added" -eq "0" ]
	then
		echo "# "                                   >> /home/${SUDO_USER}/.bashrc
		echo "# ${foglam_test}"                     >> /home/${SUDO_USER}/.bashrc
		echo "source scl_source enable rh-python36" >> /home/${SUDO_USER}/.bashrc
	fi
	source scl_source enable rh-python36

    # TODO: we may need with --no-cache-dir
	pip3 install -Ir /usr/local/fledge/python/requirements.txt

	sudo bash -c 'source scl_source enable rh-python36;pip3 install dbus-python'
	set -e
}

# Call Fledge package update script
# Any message will be written by called update script
call_package_update_script () {
    # File created by presinstall hook
    installed_version_file="/usr/local/fledge/.current_installed_version"
    if [ -s "${installed_version_file}" ]; then
        current_installed_version=`cat ${installed_version_file}`
        update_script="/usr/local/fledge/scripts/package/rpm/package_update.sh"
        # Check update script exists
        if [ -x "${update_script}" ] && [ -s "${update_script}" ] && [ -O "${update_script}" ]; then
            # Call RPM update script passing the previous version
            ${update_script} ${current_installed_version}
        fi
        # Update done: remove temp file
        rm ${installed_version_file}
    fi
}



# main
echo "Install python dependencies"
install_pip3_packages

echo "Resolving data directory"
copy_new_data

echo "Installing service script"
copy_service_file

echo "Generating certificate files"
generate_certs

echo "Generating auth certificate files"
generate_auth_certs

echo "Setting ownership of Fledge files"
set_files_ownership

# Call Fledge package update script
# TODO: DISABLED - to be implemented
#call_package_update_script

echo "Linking update task"
link_update_task

echo "Copying sudoers file"
copy_fledge_sudoer_file

echo "Enabling Fledge service"
enable_fledge_service

# Skipping the start of fledge when package is upgraded, 
# because of other related packages upgrade transaction mechanism is causing issues in Fledge (FOGL-5506).
if [ $1 == 2 ];then
    echo "Please start fledge once upgrade process is complete; using 'systemctl start fledge'"
else
    echo "Starting Fledge service"
    start_fledge_service
fi


%postun
#!/usr/bin/env bash

##--------------------------------------------------------------------------
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
##--------------------------------------------------------------------------

##--------------------------------------------------------------------------
##
## The %postun scriptlet executes just after the package is to be erased.
##
## Author: Ashish Jabble
##
##--------------------------------------------------------------------------

set -e
PKG_NAME="fledge"

remove_unused_files () {
  find /usr/local/fledge/ -maxdepth 1 -mindepth 1 -type d | egrep -v -w '(/usr/local/fledge/data)' | xargs rm -rf
}

remove_fledge_sudoer_file() {
    rm -rf /etc/sudoers.d/fledge
}

# main
if [ $1 == 1 ];then
    echo "postun scriptlet is called: ${PKG_NAME} is getting upgraded."
    # Add steps here for the upgrade case for this scriptlet
elif [ $1 == 0 ];then
    echo "postun scriptlet is called: ${PKG_NAME} is getting removed/uninstalled."
    echo "Cleanup of files"
    remove_unused_files
    echo "Remove fledge sudoers file"
    remove_fledge_sudoer_file
fi


%files
%{install_path}/*
