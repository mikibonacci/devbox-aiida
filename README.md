# devbox-aiida

A ready-to-use environment for [AiiDA](https://www.aiida.net/): PostgreSQL and RabbitMQ managed by [devbox](https://www.jetify.com/devbox), a Python virtual environment, and scripts to create the profile and to register computers and codes from YAML files.

**Do not run `devbox shell`.** Use devbox for the services and the `devbox run` scripts, and activate the environment in your own shell with `source scripts/init_hook.sh`.

## Quick start

```shell
devbox install                     # install PostgreSQL, RabbitMQ, Python
devbox run install-requirements    # create .venv, initialise PostgreSQL, install aiida-core
devbox services up -b              # start PostgreSQL and RabbitMQ
source scripts/init_hook.sh        # activate .venv and set AIIDA_PATH (every new terminal)
devbox run create-aiida-profile    # first time only: create a profile
verdi status
```

Stop with `verdi daemon stop` and `devbox services stop`.

## Shortcut

Add this to your `~/.bashrc` (or `~/.zshrc`) to jump to the folder and load the environment with one word:

```shell
alias gtd='cd /path/to/devbox_aiida && source scripts/init_hook.sh'
```

## Documentation

Full documentation (installation, services, profiles, computers and codes, troubleshooting) is in [`docs/`](docs/index.md), built with MkDocs:

```shell
source scripts/init_hook.sh
pip install -r requirements-docs.txt
mkdocs serve
```
