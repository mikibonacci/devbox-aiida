# Install additional plugins

`requirements.txt` only contains the base packages. Other plugins, especially development versions, are installed by hand in the activated environment (`source scripts/init_hook.sh`).

## Wannier90 workflows (temporary branch)

```bash
git clone https://github.com/mikibonacci/aiida-wannier90-workflows.git
cd aiida-wannier90-workflows
git checkout fix-inputpp
pip install -e .
cd ..
```

## Yambo (cleanup branch)

```bash
git clone https://github.com/mikibonacci/aiida-yambo.git
cd aiida-yambo
git checkout new_cleanup
pip install -e .
cd ..
```

!!! note
    `-e` installs the package in editable mode: changes to the cloned repository are used immediately. Clone these repositories outside `devbox_aiida/` (for example next to it), because the folder is meant to hold only the environment.

After installing a plugin, restart the daemon so that it sees the new entry points:

```bash
verdi daemon restart
```

Check that AiiDA finds the plugin:

```bash
verdi plugin list aiida.calculations
```
