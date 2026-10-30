# Plan: documentation (MkDocs) and small fixes

Status: **proposal only. Nothing in this plan has been applied.** Review it, strike what you do not want, and answer the open questions at the end.

## Decision

`devbox.json` stays as it is: **Python, the init hook and all current packages and scripts are kept.** The hook works (it creates and activates `.venv` and sets `AIIDA_PATH`); its banner on every `devbox` command is left as it is. The earlier idea of making devbox services-only is dropped.

## What I checked about the Python plugin (for the record)

Checked on a throwaway copy, since deleted:

- With `python@3.12` in devbox, the Python plugin creates `.venv` itself the first time any `devbox` command runs ("Virtual environment directory doesn't exist. Creating new one..."). It also sets `VENV_DIR`, `UV_PROJECT_ENVIRONMENT` and a `PYTHONPATH` inside the devbox environment. Your `init_hook.sh` then activates that same `.venv`. None of this is harmful.
- If you ever want to keep Python but switch off those plugin hooks, `"python@3.12": {"disable_plugin": true}` in `devbox.json` does it: no automatic `.venv`, no `VENV_DIR` / `UV_*`, and `python -m venv` still works. **Not proposed**, only recorded.

## Proposed work

### 1. Documentation (the main request)

Add `mkdocs.yml` (Material theme, same style as `aiida-yambo`), `requirements-docs.txt` (`mkdocs>=1.6,<2`, `mkdocs-material>=9.5`), and `docs/`:

```text
docs/
├── index.md                       overview, diagram, quick start
├── installation.md                first-time setup, daily use
├── how-to/
│   ├── index.md
│   ├── services.md                start/stop/inspect, ports, logs, RabbitMQ version caveat
│   ├── profiles.md                create, switch, delete, reset everything
│   ├── computers-and-codes.md     YAML layout, setup_aiida_resources.py, ssh config, gw2wannier90
│   ├── pseudopotentials.md
│   ├── jupyter.md
│   ├── plugins.md                 wannier90-workflows and yambo dev branches
│   └── troubleshooting.md
├── concepts/architecture.md       devbox for services, venv for Python, data locations
└── reference/
    ├── commands.md                devbox run scripts and scripts/*
    └── configuration.md           env vars, ports, files
```

The docs describe the setup **as it is now** (`source scripts/init_hook.sh`, `devbox run install-requirements`, `devbox run create-aiida-profile`, `devbox run install-pseudos`, `devbox services up -b`). I would build them with `mkdocs build --strict` and show you the result.

Also: add `site/` to `.gitignore`.

Added at your request while implementing:

- `.github/workflows/docs.yml`: builds the site with `mkdocs build --strict` on pushes and pull requests that touch the docs, and publishes it to GitHub Pages on pushes to `main`. It needs a one-time repository setting: Settings, Pages, Source: "GitHub Actions". Nothing is published until you push.
- The shortcut `alias gtd='cd /path/to/devbox_aiida && source scripts/init_hook.sh'` in the README and in the installation page, with a placeholder path.
- The installation order is `devbox install`, `devbox run install-requirements`, `devbox run initdb`, `devbox services up -b`, then `source scripts/init_hook.sh`. I checked that on a fresh copy, `devbox run install-requirements` creates `.venv` with devbox's Python 3.12 and installs the requirements.

Applied at your request: a guarded `initdb` in `scripts/init_hook.sh` (plus the last banner line, which used to tell you to run `initdb` by hand). Tested on a fresh throwaway copy: the first devbox command initialises the data directory, later ones do not re-run it, PostgreSQL starts without a manual `initdb`, and sourcing the hook in a plain shell skips it. The docs no longer have a manual `initdb` step.

### 2. Fix known errors in the existing text

| Where | Problem | Fix |
| --- | --- | --- |
| `services.md` | Says the RabbitMQ management UI (15672) is enabled. It is not: there is no `enabled_plugins` file, and only 5672 and 25672 listen | Correct it |
| `services.md` | Says `postgresql@latest` and a socket in `/tmp` | Real values: 17.10 and `.devbox/virtenv/postgresql/` |
| `README.md` | `source scripts init_hook.sh` (missing `/`) | `source scripts/init_hook.sh` |
| `README.md` | `pip install aiida-wannier90-workflows` after `cd` into the clone | `pip install -e .` |
| `README.md` | `pip install -e aiida-yambo` after `cd aiida-yambo` | `pip install -e .` |
| `how_to_have_aiida_ready.md` | Unfinished outline | Fold into the installation page |

`services.md` would move into `docs/how-to/services.md` (corrected), and `README.md` would be shortened to a quick start plus a pointer to the docs. I would only do this part after your OK.

## Risks

- Low: the docs and the README fixes touch no running code.
- `devbox.json`, `devbox.lock`, `scripts/init_hook.sh`, `.venv` and the services are not touched. I would only run read-only devbox commands (such as `devbox services ls`) in this folder.
- The repository path must stay short (macOS limits the PostgreSQL socket path to 103 bytes). I would document it in the troubleshooting page.
- Not verified: `verdi` completion in zsh and changing ports through `devbox services up --env`. I would mark them as untested or leave them out.

## Order of work

1. Write `docs/`, `mkdocs.yml`, `requirements-docs.txt`; build and check with you. No existing file is modified.
2. After your OK: apply section 2 (README and `services.md` fixes).

## Open questions

1. Is the documentation structure above what you want, or should it be smaller (for example one page per topic of the current README)?
2. Move `services.md` into the docs and shorten the README (section 2), or leave both files as they are?
3. Where should the docs be hosted, if anywhere (GitHub Pages, Read the Docs, nowhere)?
