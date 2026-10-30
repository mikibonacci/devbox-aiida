# Architecture

## What devbox does here

| Role | Provided by | Used how |
| --- | --- | --- |
| PostgreSQL 17 and RabbitMQ 3.8.9 | devbox packages and plugins, supervised by process-compose | `devbox services ...` |
| Python 3.12, `pip`, `gnuplot`, `watch` | devbox packages | to build `.venv` and for `devbox run` scripts |
| Python packages (`verdi`, plugins, Jupyter) | `.venv` (pip) | `source scripts/init_hook.sh` |

AiiDA and the services only talk through the network: AiiDA connects to `localhost:5432` (PostgreSQL) and `127.0.0.1:5672` (RabbitMQ).

## The init hook

`devbox.json` declares `scripts/init_hook.sh` as the devbox `init_hook`, and you also `source` it yourself. It:

1. creates `.venv`, `aiida/` and `work/` if they are missing;
2. initialises the PostgreSQL data directory if it does not exist (only inside devbox, where `initdb` is available);
3. activates `.venv`;
4. enables `verdi` tab completion (interactive shells only);
5. exports `AIIDA_PATH=<repository>/aiida`;
6. prints a short banner with the available commands.

Because it is a devbox `init_hook`, devbox runs it before every `devbox` command, which is why the banner also appears with `devbox services ls` or `devbox run ...`. That is also what lets the `devbox run` scripts find `verdi`.

!!! note "The Python plugin"
    Having `python@3.12` in `devbox.json` also activates devbox's Python plugin, which creates `.venv` the first time any `devbox` command runs and sets `VENV_DIR` and `UV_PROJECT_ENVIRONMENT`. The init hook then activates the same `.venv`.

## Why not `devbox shell`

`devbox shell` starts a new shell that replaces your own configuration: prompt, aliases, tab completion, `SHELL`. Sourcing the init hook in your shell gives you the same environment (`.venv`, `AIIDA_PATH`) without that.

## Directory layout

```text
devbox_aiida/
├── devbox.json            # packages, init hook, devbox run scripts
├── devbox.lock
├── devbox.d/              # RabbitMQ plugin configuration (rabbitmq.conf)
├── scripts/               # init_hook.sh, install_requirements.sh, setup_aiida_resources.py
├── aiida_configurations/  # computers and codes, one folder per computer
├── requirements.txt       # Python packages of .venv
├── docs/, mkdocs.yml      # this documentation
│
├── .venv/                 # Python virtual environment               (not versioned)
├── aiida/                 # AIIDA_PATH: config.json and repositories (not versioned)
├── work/                  # your notebooks and scripts               (not versioned)
└── .devbox/               # Nix profile, services state and data     (not versioned)
```

## Where the data lives

A profile is made of **two** parts, and both must be kept together:

| Part | Location |
| --- | --- |
| Database (nodes, links, attributes) | PostgreSQL cluster in `.devbox/virtenv/postgresql/data` |
| File repository (stored files) | `aiida/.aiida/repository/<profile>/` |
| Profile configuration | `aiida/.aiida/config.json` |

!!! danger "`.devbox/` contains your database"
    Deleting `.devbox/` also deletes the PostgreSQL data directory, and with it every node of your profiles. Back up (for example with `verdi archive create`) before cleaning up the folder.

## The services

- PostgreSQL comes with devbox. It listens on `localhost:5432` only, plus a Unix socket in `.devbox/virtenv/postgresql/`. Connections from the local machine use `trust` authentication, and the superuser is your operating-system user.
- RabbitMQ uses the [`jetify-com/devbox-plugins` rabbitmq plugin](https://github.com/jetify-com/devbox-plugins/tree/main/rabbitmq). It listens on port `5672` on **all** interfaces, with the default `guest` / `guest` credentials (RabbitMQ only lets `guest` log in from the local machine).

Both are started and supervised by [process-compose](https://github.com/F1bonacc1/process-compose). Paths and environment variables are listed in [Configuration and files](../reference/configuration.md).

!!! warning "Local development only"
    `trust` authentication and `guest` credentials are fine for a laptop or a workstation behind a firewall. Do not expose ports `5432` and `5672` to an untrusted network.
