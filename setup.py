"""
Setup file for Python packaging.
"""

import io
import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))
requirements = [
    "enum34;python_version<'3.4'",
    "google-resumable-media[requests]",
    "typing;python_version<'3.5'",
]
packages = [pkg for pkg in find_packages() if pkg.startswith("crux")]

version = {}
with io.open(os.path.join(here, "crux", "__version__.py"), "r", encoding="utf-8") as fh:
    exec(fh.read(), version)

with io.open("README.md", "r", encoding="utf-8") as fh:
    readme = fh.read()

setup(
    name="crux",
    packages=packages,
    version=version["__version__"],
    description="Crux Informatics API client library",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Crux Informatics, Inc.",
    author_email="python-opensource@cruxinformatics.com",
    url="https://github.com/cruxinformatics/crux-python",
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*",
    license="MIT",
    install_requires=requirements,
    keywords=["crux-python"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development",
    ],
)
