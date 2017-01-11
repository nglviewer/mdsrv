
Making a Release
================

Follow semantic versioning and make sure the changelog is up-to-date.

For non prerelease level also update [README.md](README.md) and [CHANGELOG.md](CHANGELOG.md) and make a release on github including copying the relevant info from the changelog file there.


We use [Versioneer](https://github.com/warner/python-versioneer) to automatically update the version string (of a release but also in development). This means for a release a new git tag should be created. The tag should be of the form vX.Y or vX.Y.Z and generally follow [pep440](https://www.python.org/dev/peps/pep-0440/) with a prefixed "v".

```bash
git tag  -a vX.Y -m "version X.Y"
git push
git push origin --tags
python setup.py sdist upload -r pypi  # better use twine for uploading, see below
```

To ensure a secure upload use `twine`:
```bash
# Create some distributions in the normal way:
python setup.py sdist
# Upload with twine:
twine upload dist/*
```


Development
===========

Development of the MDsrv is coordinated through the repository on [github](http://github.com/arose/mdsrv). Please use the [issue tracker](https://github.com/arose/mdsrv/issues) there to report bugs or suggest improvements.

To participate in developing for the MDsrv you need a local copy of the source code, which you can obtain by forking the [repository](https://github.com/arose/mdsrv) on github. Read about how to [fork a repository](https://help.github.com/articles/fork-a-repo/), [sync a fork](https://help.github.com/articles/syncing-a-fork/) and [start a pull request](https://help.github.com/articles/using-pull-requests/).

