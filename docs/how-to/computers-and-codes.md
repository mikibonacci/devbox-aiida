# Set up computers and codes

A computer and its codes are described by YAML files in `aiida_configurations/`, one folder per computer. `scripts/setup_aiida_resources.py` reads a folder and registers everything, skipping what already exists.

## Folder layout

```text
aiida_configurations/corvina/
├── corvina-direct-setup.yaml     # verdi computer setup --config
├── corvina-direct-config.yaml    # verdi computer configure --config
└── codes/
    ├── qe-7.5-gcc-spack@corvina-direct.yaml   # verdi code create --config
    ├── yambo-5.3.0-gcc@corvina-direct.yaml
    └── ...
```

| File | Required | Content |
| --- | --- | --- |
| `*-setup.yaml` (exactly one) | for the computer | `label`, `hostname`, `scheduler`, `transport`, `work_dir`, `mpirun_command`, ... |
| `*-config.yaml` (exactly one) | for the computer | transport options such as `host`, `backend`, `safe_interval` |
| `codes/*.yaml` | for the codes | `label`, `computer`, `filepath_executable`, `default_calc_job_plugin`, `prepend_text`, ... |

The easiest way to write them is to configure a computer or a code once by hand and export it: `verdi computer export setup LABEL file.yaml`, `verdi computer export config LABEL file.yaml`, `verdi code export LABEL file.yaml`.

## Register a computer and all its codes

```bash
python scripts/setup_aiida_resources.py aiida_configurations/corvina
```

The script:

1. skips the computer if one with the same `label` exists, otherwise runs `verdi computer setup` and `verdi computer configure <transport>`;
2. for every file in `codes/`, skips the code if `label@computer` exists, otherwise runs `verdi code create core.code.installed`.

| Option | Effect |
| --- | --- |
| `--computer-only` | Set up the computer and skip the codes |
| `--codes-only` | Register the codes and skip the computer |

You can safely run it again after adding a code file. Check the result:

```bash
verdi computer list
verdi computer test corvina-direct
verdi code list
```

!!! warning
    A code is identified by `label@computer`. Creating the same code with `verdi code create` by hand registers a second, distinct node: use the script, or check `verdi code list | grep corvina` first.

## Do it by hand

```bash
verdi computer setup --config aiida_configurations/corvina/corvina-direct-setup.yaml
verdi computer configure core.ssh_async --config aiida_configurations/corvina/corvina-direct-config.yaml
verdi code create core.code.installed --config "aiida_configurations/corvina/codes/yambo-5.3.0-gcc@corvina-direct.yaml"
```

If AiiDA asks for an optional value (for example the default memory per node), type `!` to skip it.

## Quantum ESPRESSO from your `PATH`

For executables installed on this machine:

```bash
aiida-quantumespresso setup codes localhost pw.x projwfc.x dos.x wannier90.x
```

and check them with `verdi code list`.

## Remote computers: SSH configuration

The `core.ssh_async` transport reads your `~/.ssh/config`. Each remote host must be declared there with the same name as the `host` in the `*-config.yaml` file:

```text
Host login02-ext.leonardo.cineca.it
    User mbonacci
    IdentityFile none
    ForwardAgent yes
```

## The `gw2wannier90` code on a remote machine

The `gw2wannier90` code is a Python script that must exist on the remote computer, in its own virtual environment:

- create a venv;
- clone the `aiida-yambo-wannier90` package;
- install the requirements (`numpy`, `scipy`).

For example on `aries`:

```bash
module load python/3.14.0-gcc-8.5.0-ddmg2af
python -m venv gw2wannier90-venv
source gw2wannier90-venv/bin/activate
pip install numpy scipy
git clone https://github.com/aiidaplugins/aiida-yambo-wannier90.git

# test:
python aiida-yambo-wannier90/utils/gw2wannier90.py
```

Expected output:

```text
usage: gw2wannier90.py [-h] [-o OUTPUT_SEEDNAME] [-e EXTENSIONS] [--no_sort] seedname
gw2wannier90.py: error: the following arguments are required: seedname
```
