echo "builder.sh ..."

REPO_NAME=`basename $DOC_REPO .git`

python /app/scripts/builder.py $REPO_NAME

