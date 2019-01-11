"""
Nox config for running tests.
"""
import multiprocessing

import nox

cpu_count = multiprocessing.cpu_count()

if cpu_count > 4:
    cpu_count = 4
elif cpu_count > 2 and cpu_count < 4:
    cpu_count = 2
else:
    cpu_count = 1


@nox.session(python=["3.7"])
def lint(session):
    """Run linters."""
    session.install("flake8", "flake8-import-order")
    session.install("pylint")
    session.install("-r", "requirements.txt")
    session.run("flake8", ".")
    session.run("pylint", "crux")


@nox.session(python=["2.7", "3.5", "3.6", "3.7"])
def unit(session):
    """Run unit tests."""
    session.install("pytest")
    session.install("-r", "requirements.txt")
    session.run("python", "-m", "pytest", "tests/unit")


@nox.session(python=["2.7", "3.5", "3.6", "3.7"])
def integration(session):
    """Run integration tests."""
    session.install("pytest")
    session.install("pytest-xdist")
    session.install("-r", "requirements.txt")
    session.run("python", "-m", "pytest", "-n", str(cpu_count), "tests/integration")


@nox.session(python=["3.7"])
def format_check(session):
    """Run all tests."""
    session.install("black")
    session.run("black", "--check", ".")


@nox.session(python=["3.7"])
def type_check(session):
    """Run type checks."""
    session.install("-r", "requirements.txt")
    session.install("mypy")
    session.run("mypy", "crux")
