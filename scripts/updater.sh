#! /bin/bash

echo "Updating ..."

if [ -z ${DOC_REPO} ]; then
    export DOC_REPO="git@github.com:tobyqin/auto-docsify.git"
fi

NSS_WRAPPER_PASSWD=/tmp/passwd.nss_wrapper
NSS_WRAPPER_GROUP=/etc/group
USER_HOME=/app
export NSS_WRAPPER_PASSWD
export NSS_WRAPPER_GROUP
LD_PRELOAD=/usr/lib64/libnss_wrapper.so
export LD_PRELOAD
REPO_NAME=`basename $DOC_REPO .git`

cd /app/repo

if [ ! -d $REPO_NAME ]; then
    git clone ${DOC_REPO}
fi

cd "$REPO_NAME"
git pull origin ${DOC_BRANCH}

