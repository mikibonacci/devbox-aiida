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

echo "Important: if this is the first time you run this environment, you can initialise the psql database by running: 'devbox services start && initdb'."