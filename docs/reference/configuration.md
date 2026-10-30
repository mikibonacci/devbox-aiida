# Configuration and files

## `devbox.json`

| Key | Meaning |
| --- | --- |
| `packages` | `postgresql@17.10`, `python@3.12`, `gnuplot@6.0.4`, `watch@latest`, `python312Packages.pip@latest`, `rabbitmq-server@3.8.9` |
| `include` | The RabbitMQ plugin (service definition and `devbox.d/` configuration) |
| `shell.init_hook` | Sources `scripts/init_hook.sh` before every `devbox` command |
| `shell.scripts` | `init-aiida`, `install-requirements`, `create-aiida-profile`, `install-pseudos`, `test`: see [Commands](commands.md) |

The PostgreSQL plugin is built into devbox and needs no `include`.

## Environment variables

Set by devbox (visible inside `devbox run` and the services):

| Variable | Value |
| --- | --- |
| `PGDATA` | `.devbox/virtenv/postgresql/data` |
| `PGHOST` | `.devbox/virtenv/postgresql` |
| `PGPORT` | not set: PostgreSQL uses `5432` |
| `RABBITMQ_NODENAME` | `rabbit` |
| `RABBITMQ_CONFIG_FILES` | `devbox.d/jetify-com.devbox-plugins.rabbitmq/conf.d` |
| `RABBITMQ_ENABLED_PLUGINS_FILE` | `devbox.d/jetify-com.devbox-plugins.rabbitmq/conf.d/enabled_plugins` |
| `RABBITMQ_LOG_BASE` | `.devbox/virtenv/jetify-com.devbox-plugins.rabbitmq/log` |
| `RABBITMQ_MNESIA_BASE` | `.devbox/virtenv/jetify-com.devbox-plugins.rabbitmq/mnesia` |
| `RABBITMQ_PID_FILE` | `.devbox/virtenv/jetify-com.devbox-plugins.rabbitmq/pid/.pid` |

Set by `scripts/init_hook.sh` (also in your shell when you source it):

| Variable | Value |
| --- | --- |
| `VENV_DIR` | `<repository>/.venv` |
| `AIIDA_PATH` | `<repository>/aiida` |
| `VIRTUAL_ENV`, `PATH` | set by `.venv/bin/activate` |

## Ports

| Service | Port | Interface |
| --- | --- | --- |
| PostgreSQL | `5432` | `localhost` |
| RabbitMQ (AMQP) | `5672` | all |
| RabbitMQ (inter-node and CLI tools) | `25672` | all |

## Files and folders

| Path | Versioned | Content |
| --- | --- | --- |
| `devbox.json`, `devbox.lock`, `devbox.d/` | yes | packages, services, scripts |
| `requirements.txt` | yes | packages of `.venv` |
| `requirements-docs.txt`, `mkdocs.yml`, `docs/` | yes | this documentation |
| `scripts/` | yes | init hook and helper scripts |
| `aiida_configurations/` | yes | computers and codes (YAML) |
| `.venv/` | no | Python virtual environment |
| `aiida/` | no | `AIIDA_PATH`: `.aiida/config.json`, repositories, daemon files |
| `work/` | no | your notebooks and scripts |
| `.devbox/` | no | Nix profile, service state, PostgreSQL data, RabbitMQ data and logs |
| `site/` | no | output of `mkdocs build` |

## Python requirements

`requirements.txt`:

| Package | Version |
| --- | --- |
| `aiida-core` | 2.8.0 |
| `aiida-quantumespresso` | 5.0.0 |
| `notebook` | 7.6.0 |
| `ipympl` | latest |
