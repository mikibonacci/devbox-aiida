# Services

This devbox provides two background services — **PostgreSQL** and **RabbitMQ** — managed entirely through devbox (Nix + process-compose). No system-wide installation is required or used.

---

## How services are managed

Devbox uses [process-compose](https://github.com/F1bonacc1/process-compose) under the hood to start, stop, and monitor services declared in `devbox.json`.

| Command | What it does |
|---------|-------------|
| `devbox services start` | Start all services in the background |
| `devbox services stop` | Stop all services |
| `devbox services restart` | Restart all services |
| `devbox services ls` | List services and their current status |
| `devbox services up` | Start services and stream logs to the terminal (foreground) |

Services are started automatically when you run `devbox services start` inside the devbox shell. They are **not** started by `devbox shell` alone.

---

## PostgreSQL

| Property | Value |
|----------|-------|
| Package | `postgresql@latest` (Nix) |
| Port | **5432** (default) |
| Host | `localhost` |
| Data directory | `$PGDATA` (set by devbox, typically `.devbox/virtenv/postgresql/data`) |
| Socket directory | `/tmp` |
| Superuser | your OS username (no password by default) |

### Check if it's running and which port

```bash
# Is the process alive?
pg_ctl status

# Which port is it listening on?
pg_lsclusters 2>/dev/null || psql -d postgres -c "SHOW port;"

# Low-level socket check
lsof -i :5432
```

### Key files

| File / Dir | Purpose |
|------------|---------|
| `$PGDATA/postgresql.conf` | Main configuration (port, logging, etc.) |
| `$PGDATA/pg_hba.conf` | Client authentication rules |
| `$PGDATA/postmaster.pid` | PID file — exists only while the server is running |

---

## RabbitMQ

| Property | Value |
|----------|-------|
| Package | `rabbitmq-server@latest` (Nix) |
| AMQP port | **5672** |
| Management UI port | **15672** (if management plugin is enabled) |
| Host | `localhost` |
| Default credentials | `guest` / `guest` |

RabbitMQ is included via the devbox plugin:

```json
"include": ["github:jetify-com/devbox-plugins?dir=rabbitmq"]
```

The plugin provides a pre-configured `rabbitmq.conf` at:

```
devbox.d/jetify-com.devbox-plugins.rabbitmq/conf.d/rabbitmq.conf
```

This file is the **effective configuration** loaded by the devbox-managed RabbitMQ instance. The default AMQP listener (`listeners.tcp.default = 5672`) is commented out in that file, meaning RabbitMQ falls back to its built-in default of port **5672** on all interfaces.

### Check if it's running and which port

```bash
# Official diagnostics (must be run inside devbox shell)
rabbitmq-diagnostics listeners

# Process check
rabbitmqctl status | grep -A5 listeners

# Low-level socket check
lsof -i :5672
lsof -i :15672   # management UI
```

Example output of `rabbitmq-diagnostics listeners`:

```
Interface: [::], port: 5672,  protocol: amqp,       purpose: AMQP 0-9-1 and AMQP 1.0
Interface: [::], port: 25672, protocol: clustering,  purpose: inter-node and CLI tool communication
```

### Key files

| File / Dir | Purpose |
|------------|---------|
| `devbox.d/jetify-com.devbox-plugins.rabbitmq/conf.d/rabbitmq.conf` | Effective RabbitMQ config for this devbox |
| `$RABBITMQ_LOG_BASE/` | Log directory (set by devbox plugin) |
| `$RABBITMQ_MNESIA_BASE/` | Persistent data (queues, exchanges, users) |

### Management UI

If the management plugin is enabled (it is by default in the devbox plugin), the web UI is available at:

```
http://localhost:15672
```

Login: `guest` / `guest`

---

## AiiDA connection

AiiDA is configured to use both services via the profile stored under `$AIIDA_PATH` (`./aiida`):

```
AIIDA_PATH = $PWD/aiida
```

The profile is set up with:
- **PostgreSQL** as the database backend (port 5432)
- **RabbitMQ** as the message broker (port 5672, AMQP protocol)

To inspect the active profile's service configuration:

```bash
verdi profile show
verdi status
```

`verdi status` will report green checks for both the database and the broker if the services are running correctly.
