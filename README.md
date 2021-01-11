# Crux Python Client

A Python library for interacting with the Crux platform.

The aim of this client is to be a Pythonic way to use the Crux API reliably. It covers core functionality, such as uploading and downloading files, but does not cover all API functionality. It isn't an SDK.

Python 3.6+ is recommended. Python 2.7 and 3.5 are supported but deprecated, with support planned for removal in early-2020 and mid-2020 respectively.

**This library is ALPHA.** Breaking changes are expected. Pin to a specific version when using this library, and test upgrades thoroughly.

**See [crux-python.cruxinformatics.com](https://crux-python.cruxinformatics.com/) for detailed documentation.**

## Installation

Install a recent version of Python, and a Python dependency and virtual environment manager like [pipenv](https://pipenv.readthedocs.io/en/latest/). On macOS run:

```bash
brew install python
brew install pipenv
```

Install `crux` [from PyPI](https://pypi.org/project/crux/) in a virtual environment, and get a shell in that environment:

```bash
mkdir -p crux_example
cd crux_example
pipenv install "crux==0.0.21"
pipenv shell
```
## Getting Started

Create a file, like example.py, and use the `crux` module:

```python
from crux import Crux

conn = Crux()
identity = conn.whoami()
print("I am", identity.email)
```

Run the script:

```bash
HISTCONTROL=ignoreboth
 export CRUX_API_KEY='YOUR_API_KEY'
python3 example.py
```

See the [installation](https://crux-python.cruxinformatics.com/en/latest/installation.html) and [authentication](https://crux-python.cruxinformatics.com/en/latest/authentication.html) documentation for details.

## Development

Python 3.7 is required for development, which can be installed with `brew install python`. For heavy development work, every supported version of Python must be installed, see the pyenv documentation below.

[Pipenv](https://pipenv.readthedocs.io/en/latest/) should be used to manage dependancies during development.

1. [Install Pipenv](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv), on macOS run `brew install pipenv`
2. `git clone https://github.com/cruxinformatics/crux-python.git`
3. `cd crux-python`
4. `pipenv install --dev` to install the dependancies
5. `pipenv shell` to get a shell in the virtual environment

### Multiple Python versions

To be able to run tests against all supported Python versions, you must have all supported Python versions installed. The test runner will look for binaries called `python2.7`, `python3.5`, `python3.6`, etc. There are multiple ways to install Python versions, we'll document using [pyenv](https://github.com/pyenv/pyenv).

1. `brew install pyenv` to install
2. Put `eval "$(pyenv init -)"` towards the end of the shell configuration file (~/.bashrc or ~/.bash_profile), because it manipulates `$PATH`, for example:

    ```bash
    echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
    ```

3. Open a new Terminal to get an updated shell
4. Install required/missing Python versions (this assumes you have Python 2.7 already installed, otherwise install it too):

    ```bash
    pyenv install 3.5.6
    pyenv install 3.6.6
    pyenv install 3.7.0
    ```

5. `pyenv global system 3.5.6 3.6.6 3.7.0` to make all the Python versions available
6. If you already have pipenv virtual environment, remove it with `pipenv --rm` so it detects the Python versions
7. `pipenv install --dev` to install all the dependancies
8. `pipenv shell` to get a shell in the virtual environment

### Running tests

We use [Nox](https://nox.thea.codes/en/stable/) to automate running tests, and use `make` to automate running some commands. These commands should be run within a shell created with `pipenv shell`.

```bash
# Run all tests: lint, unit, format_check
make test
# Or
nox

# Run only lint checks
make lint
# Or
nox -s lint

# Run unit tests against all available Python versions
make unit
# Or
nox -s unit

# Run integration tests agains all available Python versions
 export CRUX_API_KEY="12345"
export CRUX_API_HOST="https://api.example.com"
make integration
# Or
 export CRUX_API_KEY="12345"
export CRUX_API_HOST="https://api.example.com"
nox --s integration

# Check formatting
make format_check
# Or
nox -s format_check

# List all commands available
make
# Or
nox -l

# Run unit test only against Python 3.7
nox -s unit-3.7

# Reformat code
make format

# Generate Sphinx HTML documentation
make docs
```
