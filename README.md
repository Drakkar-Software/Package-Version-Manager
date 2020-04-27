# Package-version-manager 1.0.1

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/bf2fb2914e3148239c9cda5f1f52b6b4)](https://app.codacy.com/gh/Drakkar-Software/Package-Version-Manager?utm_source=github.com&utm_medium=referral&utm_content=Drakkar-Software/Package-Version-Manager&utm_campaign=Badge_Grade_Dashboard)

A toolkit to automate packages version update

This toolkit will:
1. Look for changes in a changelog file
2. Extract the new version number from this changelog file
3. Update the version number in readme and version identifying files
4. Create a version git branch
5. Commit the version updates in this branch
6. Log the pull request URL to merge this branch

## Installation
From PYPI
```shell script
easy_install Package-Version-Manager
```

With sources
```shell script
python -m pip install -r requirements.txt
```

## Usage:
From PYPI
```shell script
pvg -d "/my/repo/container/folder"
```

With Sources
```shell script
python cli.py -d "/my/repo/container/folder"
```

## Developers
Build package
```shell script
python setup.py sdist bdist_egg
```
