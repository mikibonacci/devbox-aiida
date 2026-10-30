# Install pseudopotentials

Pseudopotential families are managed by [`aiida-pseudo`](https://aiida-pseudo.readthedocs.io), which is installed with `aiida-quantumespresso`.

## Standard libraries

```bash
devbox run install-pseudos
```

This installs, in the default profile, the SSSP libraries (PBE and PBEsol) and the PseudoDojo libraries (scalar and fully relativistic, `upf` format). The libraries are downloaded from the internet. A library that is already installed or cannot be downloaded does not stop the script. Check the result:

```bash
aiida-pseudo list
```

## From a folder

```bash
aiida-pseudo install family <folder_name> <label_you_want> -P pseudo.upf
```

where `-P` is the pseudopotential type (`pseudo.upf` for `.upf` files). For the best results, also set the recommended cutoffs for the family, as described in the `aiida-pseudo` documentation.

!!! warning "Norm-conserving pseudopotentials for Yambo"
    The Yambo interface needs norm-conserving pseudopotentials for the Quantum ESPRESSO step: use a PseudoDojo family, not SSSP.
