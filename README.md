# auto-docsify

Deploy and host your documentation site directly from a Git repository (Documentation as Code), powered by [docsify](https://docsify.js.org).

## Why this repo

`auto-docsify` focuses on one thing: **turn a docs repository into a hosted docs site automatically**.

It will:

1. Clone your target repo.
2. Build a docsify site from `README.md` + optional `docs/` content.
3. Keep your content updated on schedule.
4. Serve the generated site on port `8080`.

## Quick start

### 1) Build image

```bash
docker build -t auto-docsify .
```

### 2) Run container

```bash
docker run --rm -p 8080:8080 \
  -e DOC_REPO=https://github.com/your-org/your-repo.git \
  -e DOC_BRANCH=main \
  auto-docsify
```

Then open `http://localhost:8080`.

> For private repos, mount SSH keys and known_hosts as needed.

## Configuration

`DOC_REPO` is required. Everything else has defaults.

| Variable | Default | Description |
|---|---|---|
| `DOC_REPO` | _(required)_ | Git repository URL. |
| `DOC_BRANCH` | `main` | Branch to clone/pull. |
| `DOC_INDEX` | `README.md` | Project entry markdown (case-sensitive). |
| `DOC_DIR` | `docs` | Docs directory; ignored when missing. |
| `DOC_REPO_URL` | _(empty)_ | Enables “Edit Document” link in pages. |
| `DOC_SITE_NAME` | repo name | Site display name. |
| `DOC_SITE_LOGO` | _(empty)_ | Logo path or absolute URL. |
| `DOC_SITE_NAV` | `Github\|https://github.com/tobyqin,Deploy Site Like This?\|https://tobyqin.cn/docsify` | Top navbar items (`name\|url,name\|url`). |
| `DOC_SITE_PATH` | value of `DOC_DIR` | Site subpath served at `/DOC_SITE_PATH`. |
| `DOC_UPDATE_INTERNAL` | `4H` | Update interval (`0` disables auto update). |
| `DOC_SITE_UPDATER` | `scripts/updater.sh` | Update script path. |
| `DOC_SITE_BUILDER` | `scripts/builder.sh` | Build script path. |

## How it works

1. Deployment starts.
2. `DOC_REPO` is cloned to `./repo`.
3. `DOC_SITE_UPDATER` is executed.
4. `DOC_SITE_BUILDER` is executed and generates site files in `./site`.
5. A scheduled update task reruns update/build by `DOC_UPDATE_INTERNAL`.
6. Final static files are served on port `8080`.

## docsify compatibility

- docsify core and core plugins are loaded from CDN using `latest` by default.
- Static local libraries are still copied as fallback assets.

## Markdown and diagrams

- Markdown authoring guide: [Mastering Markdown](https://guides.github.com/features/mastering-markdown)
- Mermaid diagrams in fenced blocks are supported.

## More docs

- [FAQ](./docs/FAQ.md)
- [Change Logs](./docs/ChangeLog.md)
