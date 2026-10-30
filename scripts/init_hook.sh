#!/usr/bin/env bash

export VENV_DIR=$PWD/.venv

if [ ! -d $VENV_DIR ]; then
    echo 'Creating virtual environment...' && python -m venv $VENV_DIR
fi

if [ ! -d aiida ]; then 
    echo 'Creating AiiDA configuration folder...' && mkdir aiida 
fi

if [ ! -d work ]; then 
    echo 'Creating work folder...' && mkdir work 
fi

# initialise the PostgreSQL data directory once (only inside devbox, where initdb exists)
if command -v initdb >/dev/null 2>&1 && [ -n "${PGDATA:-}" ] && [ ! -s "$PGDATA/PG_VERSION" ]; then
    echo 'Initialising the PostgreSQL data directory...' && initdb >/dev/null
fi

source $VENV_DIR/bin/activate && echo "Virtual environment activated: $VENV_DIR"

# setting verdi completion for bash and AiiDA path (only in interactive shells)
if [[ $- == *i* ]]; then
    eval "$(_VERDI_COMPLETE=bash_source verdi | sed 's/ -o nosort//')"
fi
export AIIDA_PATH=$PWD/aiida

echo "Your AiiDA configuration directory is here: $AIIDA_PATH"
echo "A work directory is here: $PWD/work"

echo "To start the PostgreSQL and Rabbitmq servers, run: 'devbox services start'"
echo "To create an AiiDA profile, run: 'devbox run create-aiida-profile'"

echo "Scripts available in this devbox:"
echo "  - devbox run install-requirements: Install the required Python packages for AiiDA development"
echo "  - devbox run create-aiida-profile: Create an AiiDA profile"
echo "  - devbox run install-pseudos: Install pseudos in AiiDA"
echo "  - python scripts/setup_aiida_resources.py aiida_configurations/corvina: installs corvina computer and codes in AiiDA"

echo "The PostgreSQL data directory is initialised automatically the first time you run a devbox command."