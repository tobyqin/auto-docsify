# auto-docsify

Deploy and host your document automatically from git repository, write **Documentation as Code**, powered by [docsify](https://docsify.js.org).

Go to [FAQ](./FAQ.md) for frequently asked questions.
Go to [Change Logs](./ChangeLog.md) to see features had been added.

## Supported Parameters

Beside of `DOC_REPO`, more parameters are supported.

- `DOC_REPO`, required, set to your git repo, example: `git@server/project/my-repo.git`
- `DOC_BRANCH`, default=`master`
- `DOC_INDEX`, default=`README.md`, case sensitive.
- `DOC_DIR`, default = `docs`, if no such directory in your repo we will ignore it.
- `DOC_REPO_URL`, default=(EMPTY), if provided will add an "Edit Document" link on your page.
- `DOC_SITE_NAME`, default=(EMPTY), will use doc repo name if not provided.
- `DOC_SITE_LOGO`, default=(EMPTY), example value: `docs/logo.png` or an absolute url.
- `DOC_SITE_NAV`, default=(EMPTY), top navigation menu of document site, example value: `home|http://home, about|http://about`
- `DOC_SITE_PATH`, default=(EMPTY), used in `http://doc-site/{DOC_SITE_PATH}`, use `DOC_DIR` if not provided.
- `DOC_UPDATE_INTERNAL`, default=`4H`, `0` means disable this feature.
- `DOC_SITE_UPDATER`, default=`scripts/updater.sh`, script to update repo, will be executed every `UPDATE_DOCS_INTERNAL`
- `DOC_SITE_BUILDER`, default=`scripts/builder.sh`, script to build document site, will be executed after `DOC_SITE_UPDATER`.

## How Does It Works

1. Deployment started
2. `DOC_REPO` will be cloned to `./repo`
3. `DOC_SITE_UPDATER` executed
4. `DOC_SITE_BUILDER` executed, document site will be generated in `./site`
5. Setup cron job to run step #2 and step #3 with `DOC_UPDATE_INTERNAL`
6. Document site served at `site` on port 8080, redirect user to `DOC_SITE_PATH` if visit root path.
7. Service and route will be created automatically if you are using deployment template.

## About markdown

The documents are all written by markdown.

- [A Markdown Guide](https://guides.github.com/features/mastering-markdown)

## About docsify

If you want to fully leverage docsify, please go to its official site, and ensure all files in your `DOC_DIR` is follow its structure.

[Docsify Doc helper](https://docsify.now.sh/helpers) are some enhanced markups can help you create more meaningful content.

We also support [mermaind.js](https://mermaidjs.github.io/) which can help you draw charts easily, examples:

- [Flowchart](https://mermaidjs.github.io/flowchart.html)
- [Sequence diagram](https://mermaidjs.github.io/sequenceDiagram.html)
- [Gantt diagram](https://mermaidjs.github.io/gantt.html)
