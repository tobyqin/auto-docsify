FROM  python:latest

ENV DOC_REPO="" \
    DOC_BRANCH="master" \
    DOC_INDEX="README.md" \
    DOC_DIR="docs" \
    DOC_REPO_URL="" \
    DOC_UPDATE_INTERNAL=4H \
    DOC_SITE_NAME="" \
    DOC_SITE_LOGO="" \
    DOC_SITE_NAV="" \
    DOC_SITE_PATH="" \
    DOC_SITE_UPDATER="scripts/updater.sh" \
    DOC_SITE_BUILDER="scripts/builder.sh"

COPY / /app
RUN  chmod 777 /app
WORKDIR /app

EXPOSE 8080
CMD sh "./scripts/entrypoint.sh"
