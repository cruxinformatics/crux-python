# Crux Python Client

A Python library for interacting with the Crux platform.

The aim of this module is to be a Pythonic way to use the Crux API reliably. It covers client functionality including scanning subscriptions, getting delivery status, and downloading files.

Python 3.6+ is supported.

Source code is available on GitHub at [github.com/cruxinformatics/crux-python](https://github.com/cruxinformatics/crux-python).

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
pipenv install "crux==1.3"
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

See the [installation](installation.md) and [authentication](authentication.md) documentation for details.

## Details

Details on specific topics:

- [Installation](installation.md)
- [Authentication](authentication.md)
- [Client](client.md)
- [Dataset](dataset.md)
- [Ingestion](ingestion.md)
- [Downloading](downloading.md)
- [Exception Handling](exception_handling.md)
- [Logging](logging.md)
## - [API Reference](modules.rst)
