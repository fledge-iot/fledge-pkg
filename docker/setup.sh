#!/bin/bash
#===============================================================================================
# Script Name   : setup.sh
# Description   : This script performs a setup for fledge based archive repo with non root user
# Author        : Ashish Jabble
# Email         : ashish@dianomic.com
# Version       : 1.0
# Usage         : bash setup.sh [Username ArchiveUrl Uid Gid PackagesList]
#===============================================================================================

set -eux

USERNAME="${1}"
ARCHIVE_URL="${2}"
UID="${3}"
GID="${4}"
PACKAGES="${5}"
HOME_DIR="/home/${USERNAME}"

# Update and install dependencies
apt-get -y update && \
apt-get install -y --no-install-recommends \
    rsyslog curl wget jq nginx-light gnupg logrotate acl cron

# Nginx
cp /tmp/nginx.conf /etc/nginx/nginx.conf
chown -R "${UID}:${GID}" "/etc/nginx/nginx.conf" "/var/lib/nginx"
mkdir -p /var/log/nginx
touch /var/log/nginx/{error.log,access.log}
chown -R "${UID}:${GID}" /var/log/nginx
rm -rf /tmp/nginx.conf

# fledge repo
wget -qO- http://archives.fledge-iot.org/KEY.gpg | gpg --dearmor -o /etc/apt/trusted.gpg.d/fledge.gpg
echo "deb [signed-by=/etc/apt/trusted.gpg.d/fledge.gpg] ${ARCHIVE_URL} /" > /etc/apt/sources.list.d/fledge.list
apt-get -y update && \
DEBIAN_FRONTEND=noninteractive apt-get install -y ${PACKAGES} && \
apt-get clean && rm -rf /var/lib/apt/lists/*

# Add user and group
addgroup --gid "${GID}" "${USERNAME}"
adduser --disabled-password --gecos "" --uid "${UID}" --gid "${GID}" "${USERNAME}"

# Set ownership
chown -R "${UID}:${GID}" "${FLEDGE_ROOT}"

# Configure rsyslog for user
install -o "${UID}" -g "${GID}" -m 640 /dev/null /var/log/syslog
setfacl -m u:${USERNAME}:rwX /var/log
cat <<EOF > "${HOME_DIR}/user-rsyslog.conf"
\$ActionFileDefaultTemplate RSYSLOG_TraditionalFileFormat
\$RepeatedMsgReduction on
module(load="imudp")
input(type="imudp" port="5140" address="127.0.0.1")
*.* /var/log/syslog
EOF

# Setup logrotate configuration
mkdir -p "${HOME_DIR}/logrotate.d"
cat <<EOF > "${HOME_DIR}/logrotate.d/syslog"
/var/log/syslog {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    copytruncate
}
EOF

cat <<EOF > "${HOME_DIR}/logrotate.conf"
include ${HOME_DIR}/logrotate.d
EOF
echo -e 'logrotate state -- version 2\n"/var/log/syslog" 2025-1-1-0:0:0' > "${HOME_DIR}/logrotate.status"

# Create crontab for the user and set permissions
cat <<EOF > ${HOME_DIR}/mycron
# Run logrotate daily at midnight
0 0 * * * /usr/sbin/logrotate -s ${HOME_DIR}/logrotate.status ${HOME_DIR}/logrotate.conf >> ${HOME_DIR}/cron_logrotate.log 2>&1
EOF

crontab -u "${USERNAME}" ${HOME_DIR}/mycron
setfacl -m u:${USERNAME}:rwX /var/run
chmod u+s /usr/sbin/cron
rm "${HOME_DIR}/mycron"

# Create start script
cat << EOF > "${HOME_DIR}/start.sh"
#!/bin/bash
set -eux
# Start cron daemon
cron &
# Syslog
rsyslogd -f ${HOME_DIR}/user-rsyslog.conf -i ${HOME_DIR}/rsyslog.pid & echo "rsyslogd started"
# Start nginx
nginx &
# Start Fledge
${FLEDGE_ROOT}/bin/fledge start &
tail -f /var/log/syslog
EOF
chmod +x "${HOME_DIR}/start.sh"
chown -R "${UID}:${GID}" "${HOME_DIR}"

