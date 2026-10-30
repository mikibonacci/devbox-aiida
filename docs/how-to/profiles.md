# Create and manage profiles

Start from a shell where you ran `source scripts/init_hook.sh`, with the services running (`devbox services up -b`).

## Create a profile

```bash
devbox run create-aiida-profile
```

This starts the services if they are not running, then runs `verdi presto --use-postgres`. It creates a PostgreSQL role and database, connects the RabbitMQ broker, adds a default user, and sets up and configures `localhost` as a computer. The new profile becomes the default and gets a generated name such as `presto-1`.

To choose the name, run the command yourself:

```bash
verdi presto --use-postgres --profile-name my-profile
```

Check the result:

```bash
verdi status
```

## Start the daemon

```bash
verdi daemon start
verdi daemon status
```

The daemon needs both services. After restarting the services, run `verdi daemon restart --reset`.

## Inspect and switch

```bash
verdi profile list
verdi profile show
verdi profile setdefault my-profile
verdi -p my-profile status          # use another profile for one command
```

Profiles are stored in `aiida/.aiida/config.json`; each one has its own database and file repository (see [Architecture](../concepts/architecture.md#where-the-data-lives)).

## Delete a profile

!!! danger
    This deletes the database and the repository of the profile.

```bash
verdi daemon stop
verdi profile delete --delete-data my-profile
```

## Start again from scratch

To remove **everything** (all profiles and the PostgreSQL cluster):

!!! danger
    This deletes all your AiiDA data. Create an archive first if you need it.

```bash
verdi daemon stop
devbox services stop
rm -rf .devbox/virtenv/postgresql/data aiida/.aiida
devbox services up -b        # the init hook recreates the data directory
devbox run create-aiida-profile
```
