"""Rename the template package to a new project name.

Usage:
    uv run python scripts/rename_project.py my-project
    uv run python scripts/rename_project.py my-project --dry-run

Replaces ``ds-project`` (distribution name), ``ds_project`` (import name) and
``ds-train`` (CLI command) across the project, moves ``src/ds_project`` to
``src/<new_name>`` and regenerates ``uv.lock``.
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OLD_DIST = "ds-project"
OLD_PACKAGE = "ds_project"
OLD_SCRIPT = "ds-train"

TARGETS = ["pyproject.toml", "README.md", "Makefile", "src", "tests", "notebooks"]
SUFFIXES = {".py", ".toml", ".md", ".ipynb", ".cfg", ".yml", ".yaml", ""}
NAME_RE = re.compile(r"^[a-z][a-z0-9]*([_-][a-z0-9]+)*$")


def iter_files():
    for target in TARGETS:
        path = ROOT / target
        if path.is_file():
            yield path
        elif path.is_dir():
            for file in path.rglob("*"):
                if file.is_file() and file.suffix in SUFFIXES and "__pycache__" not in file.parts:
                    yield file


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("name", help="new project name, e.g. churn-model or churn_model")
    parser.add_argument("--dry-run", action="store_true", help="show changes without writing")
    args = parser.parse_args()

    name = args.name.lower()
    if not NAME_RE.match(name):
        sys.exit(f"Invalid name {args.name!r}: use lowercase letters, digits, '-' or '_'.")

    dist = name.replace("_", "-")
    package = name.replace("-", "_")
    script = f"{dist}-train"
    replacements = [(OLD_DIST, dist), (OLD_PACKAGE, package), (OLD_SCRIPT, script)]

    old_dir = ROOT / "src" / OLD_PACKAGE
    if not old_dir.is_dir():
        sys.exit(f"{old_dir.relative_to(ROOT)} not found; the project was already renamed.")
    new_dir = ROOT / "src" / package
    if new_dir.exists():
        sys.exit(f"{new_dir.relative_to(ROOT)} already exists.")

    print(f"Renaming: {OLD_DIST} -> {dist}, {OLD_PACKAGE} -> {package}, {OLD_SCRIPT} -> {script}")

    for file in iter_files():
        text = file.read_text(encoding="utf-8")
        new_text = text
        for old, new in replacements:
            new_text = new_text.replace(old, new)
        if new_text != text:
            print(f"  update {file.relative_to(ROOT)}")
            if not args.dry_run:
                file.write_text(new_text, encoding="utf-8")

    print(f"  move   {old_dir.relative_to(ROOT)} -> {new_dir.relative_to(ROOT)}")
    if args.dry_run:
        return
    old_dir.rename(new_dir)

    if shutil.which("uv"):
        print("Regenerating uv.lock ...")
        subprocess.run(["uv", "lock"], cwd=ROOT, check=True)
    else:
        print("uv not found; run `uv lock` to regenerate the lockfile.")

    print("Done. Run `uv sync` to reinstall the package under its new name.")


if __name__ == "__main__":
    main()
