# Package-version-manager
Toolkit to automate packages version update

This toolkit will:
1. Look for changes in a changelog file
2. Extract the new version number from this changelog file
3. Update the version number in readme and version identifying files
4. Create a version git branch
5. Commit the version updates in this branch
6. Log the pull request URL to merge this branch

## Installation
```shell script
python -m pip install -r requirements.txt
```

## Usage:
```shell script
python cly.py -d "/my/repo/container/folder"
```
