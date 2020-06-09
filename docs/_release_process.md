# Release process

This Crux Python client is published to [PyPI](https://pypi.org/project/crux/). To do publish the client we cut and publish a release. This document describes the release process.

## Summary

Here is a high level summary of the steps:

1. Make a commit that bumps the version in code and documentation, open a PR, and merge the PR to master.
2. Create a *Release* in GitHub, which will also tag the version bump commit.
3. `make publish` the release to PyPI.

## Steps

### Bump version

#### Updating

There are various places in the source repository where we explicitly list the version. The most important is *crux/__version__.py*, because that contains the version used by setup.py, and therefore is the version published to PyPI. The rest of the version references are likely in documentation.

Search the code to find all references to the current version, for example:

```
$ rg -F '0.0.15'
README.md
27:pipenv install "crux==0.0.15"

docs/index.md
27:pipenv install "crux==0.0.15"

docs/installation.md
20:pipenv install "crux==0.0.15"
26:crux = "==0.0.15"
36:python3 -m pip install "crux==0.0.15"

crux/__version__.py
3:__version__ = "0.0.15"
```

Update all the versions. This could also be a good opportunity to double check that all tests pass.

#### Committing

On a branch, commit the changes with a commit message in this format:

```
Bump version to 0.0.n

BREAKING CHANGES:

- List.
- Of.
- Breaking.
- Changes.

Changes:

- List.
- Of.
- Non-breaking.
- Changes.
```

Use `git log` to view the changes since last release. The changes should be written in *imperative mood*, such as "Change X" or "Add Y". Omit the breaking changes section if there are no breaking changes.

Push the commit to a branch on your GitHub fork, open a PR, and merge the PR.

### GitHub Release and tag

Once the "bump" PR is merged, we create a GitHub release and tag the bump commit.

1. Go to [github.com/cruxinformatics/crux-python](https://github.com/cruxinformatics/crux-python) and click **releases**.
2. Click **Draft new release**.
3. In the **Tag version** field enter the version number prefixed with a *v*, e.g., `v0.0.15`. The **Target** will remain *master*, assuming the version bump commit is the latest commit on master, otherwise change the target to the bump commit.
4. In **Release title** enter the tag version, e.g., `v0.0.15`.
5. In **Describe this release** use the same change lists as in the commit body, plus Markdown syntax to make the headings bold.
6. Check the **This is a pre-release** box (until crux-python is no longer alpha or beta).
7. Click **Publish release**.


Example description:

```markdown
**BREAKING CHANGES:**

- List.
- Of.
- Breaking.
- Changes.

**Changes:**

- List.
- Of.
- Non-breaking.
- Changes.
```

### Publishing

Maintainer or Owner access to *crux* on PyPI is required for publishing.

1. `git checkout master` to use the master branch.
2. `git pull` to get the latest updates, including the version bump.
3. `git log` to make sure your are at the bump commit, otherwise checkout the tag.
4. `pipenv shell` to get a working dev environment with required dependencies to publish to PyPI.
5. `make package` will build the wheel package. This step isn't strictly required, because `make publish` will also create the package, but this provides an opportunity to make sure the version used is correct before trying to publish.
6. `make publish` to publish to PyPI.
7. Visit [pypi.org/project/crux](https://pypi.org/project/crux/) to see if the version has been published.

## Versioning

crux-python uses semantic versioning, but is currently alpha. As a result, we number the versions as 0.0.n, and only bump the last (patch) version place. Releases can have breaking changes and still only the patch version place is bumped. Once crux-python is GA, it is expected that there will be no breaking changes without a major version bump.
