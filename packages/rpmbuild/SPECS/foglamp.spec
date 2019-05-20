%define __spec_install_pre /bin/true

Name:          __NAME__
Vendor:        Dianomic Systems, Inc. <info@dianomic.com>
Version:       __VERSION__
Release:       1
BuildArch:     __ARCH__
Summary:       FogLAMP, the open source platform for the Internet of Things
License:       Apache License
Group: 	       IOT
URL:           http://www.dianomic.com

%define install_path	/usr/local

Prefix:        /usr/local
Requires:      dbus-devel, glib2-devel, boost, openssl, rh-python36, yum-utils, gcc, autoconf, curl, libtool,  rsyslog,  wget, zlib, libuuid, postgresql, avahi, sudo
AutoReqProv:   no

%description
FogLAMP, the open source platform for the Internet of Things

%pre
#!/usr/bin/env bash

##--------------------------------------------------------------------
## Copyright (c) 2019 OSIsoft, LLC
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
## Author: Ivan Zoratti, Ashwin Gopalakrishnan, Massimiliano Pinto, Stefano Simonelli
##
##--------------------------------------------------------------------

set -e

PKG_NAME="foglamp"

is_foglamp_installed () {
	set +e
    rc=`rpm -qa  2> /dev/null  | grep -c ${PKG_NAME}`
    echo $rc
    set -e
}

get_foglamp_script () {
    foglamp_script=$(rpm -ql ${PKG_NAME} | grep 'foglamp/bin/foglamp$')
    echo $foglamp_script
}

is_foglamp_running () {
    set +e
    foglamp_script=$(get_foglamp_script)
    foglamp_status_output=$($foglamp_script status 2>&1 | grep 'FogLAMP Uptime')
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
    schema_version=$(grep foglamp_schema $version_file | awk -F = '{print $2}')
    echo $schema_version
}

exists_schema_change_path () {
    echo 1
}

# main

# check if foglamp is installed
IS_FOGLAMP_INSTALLED=$(is_foglamp_installed)

# if foglamp is installed...
if [ "$IS_FOGLAMP_INSTALLED" -eq "1" ]
then
    echo "FogLAMP is already installed: this is an upgrade/downgrade."

    # exit if foglamp is running
    IS_FOGLAMP_RUNNING=$(is_foglamp_running)
    if [ "$IS_FOGLAMP_RUNNING" -eq "1" ]
    then
        echo "*** ERROR. FogLAMP is currently running. Stop FogLAMP and try again. ***"
        exit 1
    fi

    # Persist current version in case of upgrade/downgrade
    installed_version=`rpm -qi ${PKG_NAME} | grep Version |awk '{print $3}'`
    if [ "${installed_version}" ]
    then
        # Persist current FogLAMP version: it will be removed by postinstall script
        this_dir=`pwd`
        cd /usr/local/foglamp/
        echo "${installed_version}" > .current_installed_version
        cd ${this_dir}
    fi

    # check schema version file, exit if schema change path does not exist
    CURRENT_VERSION_FILE=$(get_current_version_file)
    CURRENT_SCHEMA_VERSION=$(get_schema_version $CURRENT_VERSION_FILE)
    echo "FogLAMP currently has schema version $CURRENT_SCHEMA_VERSION"
    EXISTS_SCHEMA_CHANGE_PATH=$(exists_schema_change_path)
    if [ "$EXISTS_SCHEMA_CHANGE_PATH" -eq "0" ]
    then
        echo "*** ERROR. There is no schema change path from the installed version to the new version. ***"
        exit 1
    fi

fi



%preun
#!/usr/bin/env bash

##--------------------------------------------------------------------
## Copyright (c) 2019 OSIsoft, LLC
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

set -e

PKG_NAME="foglamp"

get_foglamp_script () {
    foglamp_script=$(rpm -ql ${PKG_NAME} | grep 'foglamp/bin/foglamp$')
    echo $foglamp_script
}

stop_foglamp_service () {
    systemctl stop foglamp
}

is_foglamp_running () {
    set +e
    foglamp_script=$(get_foglamp_script)
    foglamp_status_output=$($foglamp_script status 2>&1 | grep 'FogLAMP Uptime')
    rc=$((!$?))
    echo $rc
    set -e
}

kill_foglamp () {
    set +e
    foglamp_script=$(get_foglamp_script)
    foglamp_status_output=$($foglamp_script kill 2>&1)
    set -e
}

disable_foglamp_service () {
	set +e
	/sbin/chkconfig foglamp off
    set -e
}

remove_foglamp_service_file () {
    rm -rf /etc/init.d/foglamp
}

reset_systemctl () {
    systemctl daemon-reload
    systemctl reset-failed
}

remove_pycache_files () {
    set +e
    find /usr/local/foglamp -name "*.pyc" -exec rm -rf {} \;
    find /usr/local/foglamp -name "__pycache__" -exec rm -rf {} \;
    set -e
}

remove_data_files () {
	rm -rf /usr/local/foglamp/data

}

# main

IS_FOGLAMP_RUNNING=$(is_foglamp_running)

if [ "$IS_FOGLAMP_RUNNING" -eq "1" ]
then
    echo "FogLAMP is currently running."
    echo "Stop FogLAMP service."
    stop_foglamp_service
    echo "Kill FogLAMP."
    kill_foglamp
fi

#echo "Remove data directory."
#remove_data_files
echo "Remove python cache files."
remove_pycache_files
echo "Disable FogLAMP service."
disable_foglamp_service
echo "Remove FogLAMP service script"
remove_foglamp_service_file
echo "Reset systemctl"
reset_systemctl


%post
#!/usr/bin/env bash

##--------------------------------------------------------------------
## Copyright (c) 2019 OSIsoft, LLC
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

# certificate generation defaults
SSL_NAME="foglamp"
SSL_DAYS="365"
AUTH_NAME="ca"

link_update_task() {
    echo "Changing setuid of update_task.rpm"
    chmod ugo+s /usr/local/foglamp/bin/update_task.rpm
    echo "Removing task/update"
    [ -e /usr/local/foglamp/scripts/tasks/update ] && rm  /usr/local/foglamp/scripts/tasks/update
    echo "Create link file"
    ln -s /usr/local/foglamp/bin/update_task.rpm /usr/local/foglamp/scripts/tasks/update
}

copy_foglamp_sudoer_file() {
    cp /usr/local/foglamp/bin/foglamp.sudoers_rh /etc/sudoers.d/foglamp
}

copy_service_file() {
    cp /usr/local/foglamp/extras/scripts/foglamp.service /etc/init.d/foglamp
}

enable_foglamp_service() {

	/sbin/chkconfig foglamp on
}

start_foglamp_service() {
    systemctl start foglamp
}

set_files_ownership () {
    chown root:root /etc/init.d/foglamp
    chown -R root:root /usr/local/foglamp
    chown -R ${SUDO_USER}:${SUDO_USER} /usr/local/foglamp/data

}

generate_certs () {
    if [ ! -f /usr/local/foglamp/data/etc/certs/foglamp.cert ]; then
        echo "Certificate files do not exist. Generating new certificate files."
        cd /usr/local/foglamp
        ./scripts/certificates ${SSL_NAME} ${SSL_DAYS}
    else
        echo "Certificate files already exist. Skipping generating new certificate files."
    fi
}

generate_auth_certs () {
    if [ ! -f /usr/local/foglamp/data/etc/certs/ca.cert ]; then
        echo "CA Certificate file does not exist. Generating new CA certificate file."
        cd /usr/local/foglamp
        ./scripts/auth_certificates ca ${AUTH_NAME} ${SSL_DAYS}
    else
        echo "CA Certificate file already exists. Skipping generating new CA certificate file."
    fi
    if [ ! -f /usr/local/foglamp/data/etc/certs/admin.cert ]; then
        echo "Admin Certificate file does not exist. Generating new admin certificate file."
        cd /usr/local/foglamp
        ./scripts/auth_certificates user admin ${SSL_DAYS}
    else
        echo "Admin Certificate file already exists. Skipping generating new admin certificate file."
    fi
    if [ ! -f /usr/local/foglamp/data/etc/certs/user.cert ]; then
        echo "User Certificate file does not exist. Generating new user certificate file."
        cd /usr/local/foglamp
        ./scripts/auth_certificates user user ${SSL_DAYS}
    else
        echo "User Certificate file already exists. Skipping generating new user certificate file."
    fi
}

copy_new_data () {
    if [ ! -d /usr/local/foglamp/data ]; then
        echo "Data directory does not exist. Using new data directory"
        mv /usr/local/foglamp/data.new /usr/local/foglamp/data
    else
        echo "Data directory already exists. Updating data/extras/fogbench/fogbench_sensor_coap.template.json only."
        if [ -f /usr/local/foglamp/data.new/extras/fogbench/fogbench_sensor_coap.template.json  ]; then

            cp /usr/local/foglamp/data.new/extras/fogbench/fogbench_sensor_coap.template.json /usr/local/foglamp/data/extras/fogbench/fogbench_sensor_coap.template.json
		fi
        rm -rf /usr/local/foglamp/data.new
    fi
}

install_pip3_packages () {
	set +e

	foglam_test="added by FogLamp"
	check_already_added=`cat /home/${SUDO_USER}/.bashrc | grep -c "${foglam_test}"`

	if [ "$check_already_added" -eq "0" ]
	then
		echo "# "                                   >> /home/${SUDO_USER}/.bashrc
		echo "# ${foglam_test}"                     >> /home/${SUDO_USER}/.bashrc
		echo "source scl_source enable rh-python36" >> /home/${SUDO_USER}/.bashrc
	fi
	source scl_source enable rh-python36

	pip install -Ir /usr/local/foglamp/python/requirements.txt

	sudo bash -c 'source scl_source enable rh-python36;pip install dbus-python'
	set -e
}

# Call FogLAMP package update script
# Any message will be written by called update script
call_package_update_script () {
    # File created by presinstall hook
    installed_version_file="/usr/local/foglamp/.current_installed_version"
    if [ -s "${installed_version_file}" ]; then
        current_installed_version=`cat ${installed_version_file}`
        update_script="/usr/local/foglamp/scripts/package/rpm/package_update.sh"
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

echo "Setting ownership of FogLAMP files"
set_files_ownership

# Call FogLAMP package update script
# TODO: DISABLED - to be implemented
#call_package_update_script

#TODO: DISABLED - to be implemented
#echo "Linking update task"
#link_update_task

echo "Copying sodoers file"
copy_foglamp_sudoer_file

echo "Enabling FogLAMP service"
enable_foglamp_service

echo "Starting FogLAMP service"
start_foglamp_service


%files
%{install_path}/*
