# Use Jupyter notebooks

Jupyter is part of `requirements.txt`, so it lives in `.venv`. The simplest way to get the right environment is to start it from a shell where you ran `source scripts/init_hook.sh`:

```bash
cd work
jupyter notebook
```

The notebook server then inherits `AIIDA_PATH`, and the default profile is found by `load_profile()`:

```python
from aiida import load_profile
load_profile()
```

The services must be running (`devbox services up -b`).

## Use the kernel from another Jupyter

If you start Jupyter from somewhere else (JupyterLab installed elsewhere, VS Code), install the kernel of `.venv`:

```bash
python -m ipykernel install --user --name venv --display-name "venv"
```

and select it in the notebook. A kernel started this way does not inherit `AIIDA_PATH`, so set it in the first cell of the notebook, before loading the profile:

```python
import os
os.environ["AIIDA_PATH"] = "YOUR-AIIDA-PATH"  # find it with `echo $AIIDA_PATH` in your shell

from aiida import load_profile
load_profile()
```

!!! tip
    `work/` is not versioned. Keep your notebooks and scripts there.
