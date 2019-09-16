# Crux Python Client

A Python library for interacting with the Crux platform.

The aim of this client is to be a Pythonic way to use the Crux API reliably. It covers core functionality, such as uploading and downloading files, but does not cover all API functionality. It isn't an SDK.

Python 3.6+ is recommended. Python 2.7 and 3.5 are supported but deprecated, with support planned for removal in early-2020 and mid-2020 respectively.

**This library is ALPHA.** Breaking changes are expected. Pin to a specific version when using this library, and test upgrades thoroughly.

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
pipenv install "crux==0.0.12"
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
- [Searching](searching.md)
- [Ingestion](ingestion.md)
- [Downloading](downloading.md)
- [Uploading](uploading.md)
- [Stitching](stitching.md)
- [Labels](labels.md)
- [Tables](tables.md)
- [Resource Permissions](permissions.md)
- [Exception Handling](exception_handling.md)
- [Logging](logging.md)
- [API Reference](modules.rst)
