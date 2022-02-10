# glyph

A proof-of-concept package manager for Cairo contracts/libraries. Distribution through pypi. Installation through existing package managers -- pip, pipenv, poetry.

Intended to be a lightweight layer on top of existing python package management. Sole responsibility is collecting contracts/libraries registered to the `contracts` [namespace package](https://packaging.python.org/en/latest/guides/creating-and-discovering-plugins/#using-namespace-packages), and copying their contents to a new `contracts/lib` folder.

> NOTE: solely experimental to play around one potential strategy, doubtful that this would be a real package management solution for the ecosystem

## Usage

Install with `pip install cairo-glyph`. Additionally, `pip install cairo-nile` and `nile init` to intialize a starter project.

Check out the help command (auto-gen from code, will always be more up to date than this README):
```
(venv) sam@sam:~/dev/eth/tmp$ glyph --help
Usage: glyph [OPTIONS] COMMAND [ARGS]...

  A proof-of-concept package manager for Cairo.

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.
  --help                Show this message and exit.

Commands:
  clean  Remove everything in the lib directory
  use    Install one or all added cairo packages in the project
```

Use all libraries installed to the venv:
```
(venv) sam@sam:~/dev/eth/tmp$ glyph use --all
🔎 Discovering installed contracts...

✅ Done.
```

For now, nothing is installed. To change that, do a `pip install cairo-placeholder`

Then do it again:
```
(venv) $ glyph use --all
🔎 Discovering installed contracts...

 • Using contracts.placeholder

✅ Done.
```

If we inspect our project directory we now see it's installed in a `contracts/lib` folder:

```
├── accounts.json
├── contracts
│   ├── contract.cairo
│   └── libs
│       └── placeholder
│           └── contract.cairo
├── Makefile
├── tests
│   └── test_contract.p
```

🥳

## Your Own Library Setup

In order to allow your contracts to be installed, a few conventions must be followed.

```
contracts                # The "namespace package" that the contracts are installed to
└── placeholder          # The library you are distributing
    ├── contract.cairo
    └── __init__.py      # Required to be installable.
setup.py                 # The installer
```

The actual `setup.py` will look something like this:

```python
from setuptools import setup


setup(
    name="placeholder",

    version="1",
    description="",
    long_description="",

    author="Jane Doe",
    author_email="author@example.com",

    license="MIT License",

    packages=["contracts.placeholder"],
    # Include all extra package data. Possible to include *.cairo only
    package_data={"": ["*"]},
    zip_safe=False,
)
```

If using poetry, have pyproject.toml like:

```
[tool.poetry]
name = "cairo-placeholder"
version = "0.0.2"
description = "Example project for cairo-glyph"
authors = ["Your Name <you@example.com>"]
license = "MIT License"
readme = "README.md"
packages = [
    { include = "contracts/*" },
]

[tool.poetry.dependencies]
python = "^3.7"
cairo-nile = "^0.3.0"

[tool.poetry.dev-dependencies]

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
```

Once distributed on pypi, one could:
```
(venv) $ pip install cairo-glyph cairo-placeholder
...
(venv) $ glyph use placeholder
🔎 Discovering installed contracts...

 • Using contracts.placeholder

✅ Done.
```

Adding the following to your project:
```
contracts/
└── libs
    └── placeholder
        └── contract.cairo
```