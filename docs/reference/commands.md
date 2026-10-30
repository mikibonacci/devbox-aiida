# Commands and scripts

## devbox

| Command | Purpose |
| --- | --- |
| `devbox install` | Install the pinned packages |
| `devbox run -- <command>` | Run any command in the devbox environment, for example `psql` or `rabbitmqctl` |
| `devbox services up -b` | Start PostgreSQL and RabbitMQ in the background |
| `devbox services ls` | List the services |
| `devbox services attach` | Open the process-compose interface |
| `devbox services restart` | Restart the services |
| `devbox services stop` | Stop the services |

## `devbox run` scripts (from `devbox.json`)

| Script | Purpose |
| --- | --- |
| `devbox run install-requirements` | `pip install -r requirements.txt` in `.venv` (`scripts/install_requirements.sh`) |
| `devbox run create-aiida-profile` | Start the services if needed, then `verdi presto --use-postgres` |
| `devbox run install-pseudos` | Install the SSSP and PseudoDojo families (see [Pseudopotentials](../how-to/pseudopotentials.md)) |
| `devbox run init-aiida` | Run `scripts/init_hook.sh` inside devbox |
| `devbox run test` | Placeholder: prints an error and exits |

## Scripts

| Script | Run with | Purpose |
| --- | --- | --- |
| `scripts/init_hook.sh` | `source` | Create and activate `.venv`, initialise the PostgreSQL data directory if needed, set `AIIDA_PATH`, enable `verdi` completion. Also run by devbox before every command |
| `scripts/install_requirements.sh` | via `devbox run install-requirements` | Install `requirements.txt` |
| `scripts/setup_aiida_resources.py <dir>` | `python` | Register the computer and codes of a folder in `aiida_configurations/` (`--computer-only`, `--codes-only`). See [Computers and codes](../how-to/computers-and-codes.md) |

## Documentation

```bash
source scripts/init_hook.sh
pip install -r requirements-docs.txt
mkdocs serve        # live preview at http://127.0.0.1:8000
mkdocs build        # static site in site/
```
