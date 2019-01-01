# Crux Python Client

The Crux Python Client, provided as the `crux` Python package, it a way to interact with the Crux platform from Python. It provides functionality such as uploading, downloading, and searching for files.

## Installation (macOS)

Install a recent version of Python, and a Python dependency and virtual environment manager:

```bash
brew install python
brew install pipenv
```

Install `crux` in a virtual environment, and get a shell in that environment:

```bash
pipenv install "crux==0.0.2"
pipenv shell
```
## Getting Started

Create a file, like example.py, and use the `crux` module:

```python
import os

from crux import Crux

conn = Crux(api_key="YOUR_API_KEY")
identity = conn.whoami()
print("I am", identity.email)
```

Run the script:

```bash
python3 example.py
```

## Examples

Examples for specific topics:
- [Installation](installation.md)
- [Authentication](authentication.md)
- [Searching](searching.md)
- [Downloading](downloading.md)
- [Uploading](uploading.md)
- [Stitching](stitching.md)
- [Labels](labels.md)
- [Tables](tables.md)
- [Resource Permissions](resource_permissions.md)
- [Exception Handling](exception_handling.md)
- [API Reference](modules.rst)
