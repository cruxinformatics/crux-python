# Installation

The `crux` package can be installed with `pip`. For most application development it should be installed within a virtual environment.

## With pipenv

[Pipenv](https://pipenv.readthedocs.io/en/latest/) is a tool for managing Python virtual environments and dependancies.

On macOS is it recommened that you install Pipenv with [Homebrew](https://brew.sh/):

```bash
brew install pipenv
```

See the [Pipenv installation instructions](https://pipenv.readthedocs.io/en/latest/install/) for other operating systems.

Once Pipenv is installed, change into the root of your application directory and run:

```bash
pipenv install "crux==0.0.10"
```

This will add a line to the `[packages]` section of your Pipfile, or create a new Pipfile if one doesn't exist.

```ini
crux = "==0.0.10"
```

## With venv and pip

Alternatively you can create a virtual environment with Python 3's [venv module](https://docs.python.org/3/tutorial/venv.html) and install `crux` with `pip`.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install "crux==0.0.10"
python3 -m pip freeze > requirements.txt
```
