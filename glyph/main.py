import importlib
import os
import pkgutil
import shutil
from pathlib import Path
from typing import List, Optional

import typer

import contracts


app = typer.Typer(help="A proof-of-concept package manager for Cairo.")


@app.command()
def clean(
    force: bool = typer.Option(
        default=False,
        prompt="❗ Are you sure you want to delete the lib folder?",
        confirmation_prompt=True,
        help="If set, no confirmation dialog.",
    ),
):
    """Remove everything in the lib directory"""
    if not force:
        raise typer.Abort()

    project_contracts_dir = Path(os.getcwd()) / "contracts"
    project_libs_dir = project_contracts_dir / "libs"
    shutil.rmtree(project_libs_dir, ignore_errors=True)
    typer.echo("🔥 Deleted.")


@app.command()
def use(
    library: Optional[str] = typer.Argument(
        default=None, help="A single installed cairo library to add to the project."
    ),
    all: bool = typer.Option(
        default=False, help="Add all installed contracts to the project"
    ),
):
    """Install one or all added cairo packages in the project"""
    if not all and not library:
        typer.echo("🚨 Error: must provide a library name or use --all")
        raise typer.Abort()

    typer.echo(f"🔎 Discovering installed contracts...\n")
    discovered_plugins = {
        name: importlib.import_module(name) for _, name, _ in iter_namespace(contracts)
    }

    bullet = typer.style(" • ", fg=typer.colors.BRIGHT_GREEN, bold=True)

    # Filter plugins to only the one, if specified
    _library = f"contracts.{library}"
    if not all and _library not in discovered_plugins:
        typer.echo("🚨 Error: library not installed in venv")
        raise typer.Abort()
    elif not all:
        discovered_plugins = {_library: discovered_plugins[_library]}

    for name in discovered_plugins:
        colored_name = typer.style(name, fg=typer.colors.CYAN, bold=True)
        typer.echo(bullet + "Using " + colored_name)
        library_directory = Path(discovered_plugins[name].__path__[0])
        _install_one(library_directory)

    typer.echo("\n✅ Done.")


def iter_namespace(ns_pkg):
    # https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/#using-namespace-packages
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def _install_one(library_in_venv: Path) -> None:
    project_contracts_dir = Path(os.getcwd()) / "contracts"
    try:
        os.mkdir(project_contracts_dir)
    except FileExistsError:
        pass

    project_libs_dir = project_contracts_dir / "libs"
    try:
        os.mkdir(project_libs_dir)
    except FileExistsError:
        pass

    def _ignore_python_artifacts(src: str, names: List[str]) -> List[str]:
        return ["__init__.py", "__pycache__"]

    try:
        shutil.copytree(
            src=library_in_venv,
            dst=project_libs_dir / library_in_venv.name,
            ignore=_ignore_python_artifacts,
        )
    except FileExistsError:
        pass


if __name__ == "__main__":
    app()
