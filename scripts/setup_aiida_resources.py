#!/usr/bin/env python
"""Setup an AiiDA computer and its codes from a configuration directory.

Usage:
    python scripts/setup_aiida_resources.py <config_dir> [--codes-only] [--computer-only]

Example:
    python scripts/setup_aiida_resources.py aiida_configurations/corvina

The config_dir must contain:
  - exactly one file matching *-setup.yaml  (verdi computer setup)
  - exactly one file matching *-config.yaml (verdi computer configure)
  - a codes/ subdirectory with *.yaml files  (verdi code create)
"""

import argparse
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required: pip install pyyaml")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    """Run a shell command, printing it first."""
    print(f"  $ {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout.strip():
        print(result.stdout.strip())
    if result.stderr.strip():
        print(result.stderr.strip(), file=sys.stderr)
    if check and result.returncode != 0:
        sys.exit(f"Command failed (exit {result.returncode})")
    return result


def computer_exists(label: str) -> bool:
    result = run(["verdi", "computer", "show", label], check=False)
    return result.returncode == 0


def code_exists(label: str, computer_label: str) -> bool:
    """Check if a code with this label@computer already exists."""
    result = run(["verdi", "code", "list", "--raw"], check=False)
    target = f"{label}@{computer_label}"
    return any(target in line for line in result.stdout.splitlines())


def load_yaml(path: Path) -> dict:
    with path.open() as f:
        return yaml.safe_load(f)


# ---------------------------------------------------------------------------
# Setup computer
# ---------------------------------------------------------------------------

def setup_computer(config_dir: Path) -> str | None:
    """Run 'verdi computer setup' and 'verdi computer configure'.

    Returns the computer label, or None if skipped.
    """
    setup_files = sorted(config_dir.glob("*-setup.yaml"))
    config_files = sorted(config_dir.glob("*-config.yaml"))

    if not setup_files:
        print("[computer] No *-setup.yaml found – skipping computer setup.")
        return None
    if len(setup_files) > 1:
        sys.exit(f"[computer] Multiple *-setup.yaml files found: {setup_files}. Aborting.")

    setup_file = setup_files[0]
    setup_data = load_yaml(setup_file)
    label = setup_data.get("label")
    transport = setup_data.get("transport")

    if not label:
        sys.exit("[computer] 'label' field missing from setup yaml.")

    print(f"\n[computer] Processing computer: {label}")

    if computer_exists(label):
        print(f"[computer] '{label}' already exists – skipping setup.")
        return label

    # --- setup ---
    print("[computer] Running: verdi computer setup")
    run(["verdi", "computer", "setup", "--config", str(setup_file)])

    # --- configure ---
    if not config_files:
        print("[computer] No *-config.yaml found – skipping configure step.")
        return label

    if len(config_files) > 1:
        sys.exit(f"[computer] Multiple *-config.yaml files found: {config_files}. Aborting.")

    config_file = config_files[0]

    if not transport:
        sys.exit("[computer] 'transport' field missing from setup yaml – cannot configure.")

    print(f"[computer] Running: verdi computer configure {transport}")
    run(["verdi", "computer", "configure", transport, "--config", str(config_file), "--non-interactive"])

    print(f"[computer] '{label}' set up and configured successfully.")
    return label


# ---------------------------------------------------------------------------
# Setup codes
# ---------------------------------------------------------------------------

def setup_codes(config_dir: Path, computer_label: str | None) -> None:
    codes_dir = config_dir / "codes"
    if not codes_dir.is_dir():
        print("[codes] No codes/ directory found – skipping code setup.")
        return

    code_files = sorted(codes_dir.glob("*.yaml"))
    if not code_files:
        print("[codes] No yaml files found in codes/ – nothing to do.")
        return

    print(f"\n[codes] Found {len(code_files)} code file(s) in {codes_dir}")

    for code_file in code_files:
        code_data = load_yaml(code_file)
        label = code_data.get("label")
        comp = code_data.get("computer") or computer_label

        if not label:
            print(f"[codes] WARNING: 'label' missing in {code_file.name} – skipping.")
            continue

        print(f"\n[codes] Processing code: {label}@{comp}")

        if comp and code_exists(label, comp):
            print(f"[codes] '{label}@{comp}' already exists – skipping.")
            continue

        run(["verdi", "code", "create", "core.code.installed",
             "--config", str(code_file), "--non-interactive"])
        print(f"[codes] '{label}' created successfully.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("config_dir", type=Path, help="Path to the configuration directory (e.g. aiida_configurations/corvina)")
    parser.add_argument("--codes-only", action="store_true", help="Skip computer setup; only register codes.")
    parser.add_argument("--computer-only", action="store_true", help="Skip code registration; only set up the computer.")
    args = parser.parse_args()

    config_dir = args.config_dir.resolve()
    if not config_dir.is_dir():
        sys.exit(f"Configuration directory not found: {config_dir}")

    computer_label = None

    if not args.codes_only:
        computer_label = setup_computer(config_dir)

    if not args.computer_only:
        # If codes-only, try to infer computer label from a code yaml
        if computer_label is None:
            code_files = list((config_dir / "codes").glob("*.yaml")) if (config_dir / "codes").is_dir() else []
            if code_files:
                computer_label = load_yaml(code_files[0]).get("computer")

        setup_codes(config_dir, computer_label)

    print("\nDone.")


if __name__ == "__main__":
    main()
