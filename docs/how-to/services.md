# Manage the services

PostgreSQL and RabbitMQ are declared by devbox and supervised by [process-compose](https://github.com/F1bonacc1/process-compose). The commands below work from your normal shell.

## Start, stop, inspect

| Command | What it does |
| --- | --- |
| `devbox services up -b` | Start all services in the background |
| `devbox services up` | Start all services in the foreground, showing the process-compose interface |
| `devbox services ls` | List the services and their status |
| `devbox services attach` | Open the process-compose interface of the running services |
| `devbox services restart` | Restart all services (or the one you name) |
| `devbox services stop` | Stop all services |

Three processes run: `postgresql`, `rabbitmq` and `rabbitmq-logs`. The last one only follows the RabbitMQ log file; it may restart a few times while RabbitMQ boots, until the log file exists. This is harmless.

!!! tip
    Stop the AiiDA daemon before stopping the services (`verdi daemon stop`), and start it again afterwards (`verdi daemon start`).

## PostgreSQL

| Property | Value |
| --- | --- |
| Version | 17.10 (pinned in `devbox.json`) |
| Host and port | `localhost`, `5432` |
| Data directory (`PGDATA`) | `.devbox/virtenv/postgresql/data` |
| Socket directory (`PGHOST`) | `.devbox/virtenv/postgresql/` |
| Superuser | your operating-system user, no password |

The data directory is created automatically, once, by the init hook the first time you run a `devbox` command (it runs `initdb` if `PG_VERSION` is missing).

Open a SQL prompt, for example to list the databases:

```bash
devbox run -- psql -d postgres
```

Every AiiDA profile created with `verdi presto --use-postgres` gets its own role and database named `aiida-<profile>`.

## RabbitMQ

| Property | Value |
| --- | --- |
| Version | 3.8.9 (pinned in `devbox.json`) |
| AMQP port | `5672` |
| Credentials | `guest` / `guest` |
| Configuration | `devbox.d/jetify-com.devbox-plugins.rabbitmq/conf.d/rabbitmq.conf` |
| Data (`mnesia`) and logs | `.devbox/virtenv/jetify-com.devbox-plugins.rabbitmq/` |

The configuration file shipped by the plugin contains only comments, so RabbitMQ runs with its defaults. The management web interface is **not** enabled.

Diagnostics:

```bash
devbox run -- rabbitmq-diagnostics listeners
devbox run -- rabbitmqctl list_queues
```

!!! warning "Do not upgrade RabbitMQ blindly"
    Starting from RabbitMQ 3.8.15 the broker enforces an acknowledgement timeout on consumers (30 minutes by default), which long AiiDA processes can hit. The pinned 3.8.9 predates it. If you change the version, set `consumer_timeout` in `rabbitmq.conf` as described in the AiiDA documentation.

## Logs

| File | Content |
| --- | --- |
| `.devbox/compose.log` | Output of all services (it grows over time) |
| `.devbox/virtenv/jetify-com.devbox-plugins.rabbitmq/log/` | RabbitMQ logs |

## Change a port

The plugins read their ports from environment variables, which you can override for one run:

```bash
devbox services up -b --env PGPORT=5433
```

or permanently with an `env` section in `devbox.json`:

```json
"env": {
  "PGPORT": "5433"
}
```

!!! warning
    `verdi presto` looks for the default ports `5432` and `5672`. If you change them, create the profile by hand with `verdi profile setup core.psql_dos`.
