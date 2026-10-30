# Troubleshooting

Start with:

```bash
devbox services ls
source scripts/init_hook.sh && verdi status
```

## Unix-domain socket path is too long

PostgreSQL fails to start and `.devbox/compose.log` contains:

```text
Unix-domain socket path ".../.devbox/virtenv/postgresql/.s.PGSQL.5432" is too long (maximum 103 bytes)
```

The socket lives inside the repository, and the operating system limits its path. Move the repository to a shorter path (for example `~/devbox_aiida`). Then recreate `.venv`, because a virtual environment contains absolute paths: `rm -rf .venv`, then `devbox run install-requirements`.

## Port already in use

```bash
lsof -i :5432   # PostgreSQL
lsof -i :5672   # RabbitMQ
```

Another PostgreSQL (Homebrew, Postgres.app) or RabbitMQ is using the port. Stop it, or [change the port](services.md#change-a-port).

## PostgreSQL does not start after a crash

If the machine lost power or the process was killed, a stale `postmaster.pid` may prevent the start. Make sure that no PostgreSQL process is using this data directory, then remove the file:

```bash
ps aux | grep "[p]ostgres -k"
rm .devbox/virtenv/postgresql/data/postmaster.pid
```

## `verdi status` shows the broker or the database down

1. Check that the services run: `devbox services ls`.
2. Restart them if needed: `devbox services restart`.
3. Reset the daemon: `verdi daemon restart --reset`.

## The daemon will not start

Check that `verdi status` reports PostgreSQL and RabbitMQ in green, then look at the daemon log:

```bash
verdi daemon logshow
```

## `verdi` tab completion does not work

Completion is enabled by the init hook in interactive shells and needs bash 4.4 or newer. macOS ships bash 3.2: install a recent bash (for example with Homebrew) and use it as your shell. Do not use `devbox shell` to work around it: it is the shell replacement that this setup avoids.

## After moving or renaming the folder

Two things contain absolute paths and must be fixed:

- the virtual environment: `rm -rf .venv`, then `devbox run install-requirements`;
- the file repository path stored in `aiida/.aiida/config.json` for each profile (`repository_uri`). Edit it, or move the folder back.

## The PostgreSQL data directory was not created

The init hook creates it the first time you run a `devbox` command. Check that `.devbox/virtenv/postgresql/data/PG_VERSION` exists. If not, run any devbox command (for example `devbox services ls`) and look for the line "Initialising the PostgreSQL data directory...", or run `devbox run initdb` by hand. If the directory already exists, `initdb` refuses to run: this is harmless and the existing database is untouched.

## `.devbox/compose.log` is huge

It records the output of all services and grows indefinitely. With the services stopped, you can delete or truncate it:

```bash
devbox services stop
: > .devbox/compose.log
```

## "New devbox available"

This message appears at every `devbox` command and is harmless. Update with `devbox version update` when you want to.
