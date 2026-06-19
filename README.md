# Devbox for ready to use AiiDA

The idea is to have a ready to use environment, with initial hooks and cmdline tools to automatically setup AiiDA stuff, like computer and codes, profiles, connect to the right postgres, rabbitmq. In this way, the user just needs to provide information (minimal) about the computer and codes, via yaml files.
The only additional thing to understand is if we can use jupyter notebook kernels of the devbox environment. If so, I think everything is in place.

## Devbox installation and usage

For the installation, check this link: https://www.jetify.com/docs/devbox/installing-devbox.
Once you have it, just run `devbox shell` inside this directory, to start installing the services and needed packages.

## AiiDA quick installation

Just run:

```shell
devbox run install-requirements
```

## Quickly setting up and AiiDA profile with full functionalities

You can create a profile with all functionalities (postgres, rabbitmq), by running:

```shell
devbox run create-aiida-profile # script to run both the above commands.
```

It is important that the services stay up when you use AiiDA (the can be turned off by running `devbox services stop`). So, when you use AiiDA, be sure to manually run `devbox services up -b` (or without the `-b` if you want to check them).

To install QE codes you have in your PATH:

```shell
aiida-quantumespresso setup codes localhost pw.x projwfc.x dos.x wannier90.x
```

and check them via `verdi code list`.

## Using Jupyter notebooks

When using Jupyter notebooks, you need to install the kernel (and use it in the notebooks):

```shell
python -m ipykernel install --user --name venv --display-name "venv"
```

If this does not work, for each notebook the first block should be:

```python
import os
os.environ["AIIDA_PATH"] = "YOUR-AIIDA-PATH" # find it via `echo $AIIDA_PATH` in the devbox shell or by running `devbox run echo $AIIDA_PATH`.

from aiida import load_profile
load_profile()
```