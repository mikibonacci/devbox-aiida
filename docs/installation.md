# Installation

## Prerequisites

- [devbox](https://www.jetify.com/docs/devbox/installing-devbox) (this also installs Nix).
- A **short path** for this folder. PostgreSQL creates a Unix socket inside it, and macOS limits the socket path to 103 bytes (see [Troubleshooting](how-to/troubleshooting.md#unix-domain-socket-path-is-too-long)).

## First-time setup

Run these from the root of the repository, in your normal shell.

1. **Install the packages.**

    ```bash
    devbox install
    ```

    This installs PostgreSQL 17, RabbitMQ 3.8.9, Python 3.12 and a few tools pinned in `devbox.json`.

2. **Create the virtual environment, initialise PostgreSQL and install the requirements.**

    ```bash
    devbox run install-requirements
    ```

    The first `devbox` command creates `.venv` with the Python of devbox, the `aiida/` and `work/` folders, and the PostgreSQL data directory (the init hook runs `initdb` once, if the directory does not exist yet). The script then runs `pip install -r requirements.txt` in it (`aiida-core`, `aiida-quantumespresso`, Jupyter).

3. **Start PostgreSQL and RabbitMQ.**

    ```bash
    devbox services up -b
    devbox services ls
    ```

4. **Load the environment in your shell.**

    ```bash
    source scripts/init_hook.sh
    ```

    This activates `.venv`, sets `AIIDA_PATH` to the `aiida/` folder, and enables `verdi` tab completion in interactive shells. It does not enter the devbox shell. Repeat it in every new terminal (see the shortcut below).

5. **Create a profile** (only once).

    ```bash
    devbox run create-aiida-profile
    ```

    It starts the services if needed and runs `verdi presto --use-postgres`. Then check:

    ```bash
    verdi status
    ```

    All entries except the daemon should be green. Start the daemon with `verdi daemon start`.

## Shortcut

Add an alias to your `~/.bashrc` (or `~/.zshrc`) to go to the folder and load the environment with one word. Replace the path with the location of your checkout:

```bash
alias gtd='cd /path/to/devbox_aiida && source scripts/init_hook.sh'
```

## Daily use

```bash
devbox services up -b       # when the services are not running
gtd                         # or: cd devbox_aiida && source scripts/init_hook.sh
verdi status
```

When you have finished, stop the daemon before the services:

```bash
verdi daemon stop
devbox services stop
```

## Next steps

- [Install pseudopotentials](how-to/pseudopotentials.md)
- [Set up computers and codes](how-to/computers-and-codes.md)
- [Use Jupyter notebooks](how-to/jupyter.md)
