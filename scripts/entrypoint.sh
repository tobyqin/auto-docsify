#! /bin/bash

echo "Start ..."

if [ -z ${DOC_REPO} ]; then
    export DOC_REPO="git@github.com:tobyqin/auto-docsify.git"
fi

NSS_WRAPPER_PASSWD=/tmp/passwd.nss_wrapper
NSS_WRAPPER_GROUP=/etc/group
USER_HOME=/app

if [ ! -f ${NSS_WRAPPER_PASSWD} ]; then
    cp /etc/passwd $NSS_WRAPPER_PASSWD
    echo "${USER_NAME:-doc}:x:$(id -u):0:${USER_NAME:-doc} user:${USER_HOME}:/sbin/nologin" >>$NSS_WRAPPER_PASSWD
fi

export NSS_WRAPPER_PASSWD
export NSS_WRAPPER_GROUP
LD_PRELOAD=/usr/lib64/libnss_wrapper.so
export LD_PRELOAD

cp -r /app/scripts/.ssh /app
chmod 600 /app/.ssh/id_rsa

mkdir -p /app/site
mkdir -p /app/repo

cd /app/repo
git clone ${DOC_REPO}

cd /app
sh ${DOC_SITE_UPDATER}
sh ${DOC_SITE_BUILDER}

cd /app/site
python -m http.server 8080
