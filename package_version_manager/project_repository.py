#  Drakkar-Software Package-Version-Manager
import re
from os.path import join, isfile, sep
from git import Repo
from logging import getLogger

from package_version_manager.constants import CHANGELOG_FILE, VERSION_REGEX, VERSION_CONSTANT_FILE, VERSION_CONSTANT, \
    README_FILE, VERSION_COMMIT_PREFIX, VERSION_BRANCH_PREFIX, REMOTE_NAME


class ProjectRepository:
    VERSION_REGEX = None

    def __init__(self, entry, config):
        self.entry = entry
        self.config = config
        self.logger = getLogger(self.get_name())
        self.repo = Repo(entry.path)
        self.new_version = None
        self.previous_version = None
        self.update_branch = None
        self.updated_files = []
        self.remote = None
        if ProjectRepository.VERSION_REGEX is None:
            ProjectRepository.VERSION_REGEX = re.compile(self.config[VERSION_REGEX].strip())

    def is_version_to_update(self):
        # version is to update when changelog has a new entry
        changelog_file = join(self.entry, self.config[CHANGELOG_FILE])
        if isfile(changelog_file):
            try:
                diff = self.repo.git.diff(self.config[CHANGELOG_FILE])
                matched_groups = ProjectRepository.VERSION_REGEX.findall(diff)
                if matched_groups:
                    self.new_version = matched_groups[0]
                    self.logger.info(f"New version found: {self.new_version}")
                    self._find_previous_version(changelog_file)
                    self.updated_files.append(changelog_file)
                    return True
            except Exception as e:
                self.logger.error(f"Error while analysing repository, this one will be ignored ({e})")
        return False

    def update_version(self):
        self._update_version_constant()
        self._update_readme_file()

    def commit_in_version_branch(self):
        self.update_branch = f"{self.config[VERSION_BRANCH_PREFIX].strip()}{self.new_version}"
        self.repo.git.checkout(b=self.update_branch)
        for file_path in self.updated_files:
            to_add_file = file_path.split(self.entry.path + sep)[-1]
            self.repo.git.add(to_add_file)
        self.repo.index.commit(f"{self.config[VERSION_COMMIT_PREFIX].strip()}{self.new_version}")

    def push_version_branch(self):
        remote = self.config[REMOTE_NAME].strip()
        self.remote = self.repo.remote(name=remote)
        self.remote.push(self.update_branch)
        self.logger.info(f"Pushed {self.update_branch} branch to {remote}")

    def create_pull_request(self):
        repo_url = self.remote.url.split(".git")[0]
        pull_request_link = f"{repo_url}/compare/{self.update_branch}?expand=1"
        self.logger.info(f"Create a pull request using the following link: {pull_request_link}")

    def get_name(self):
        return f"{ProjectRepository.__name__}[{self.entry.name}]"

    def _find_previous_version(self, changelog_file):
        with open(changelog_file) as f:
            changelog_content = f.read()
            versions = ProjectRepository.VERSION_REGEX.findall(changelog_content)
            self.previous_version = versions[1]

    def _update_version_constant(self):
        constant_version_file = join(self.entry, self.sanitize_repo_name(), self.config[VERSION_CONSTANT_FILE])
        to_replace_str = f"{self.config[VERSION_CONSTANT]} = \"{self.previous_version}\""
        new_str = f"{self.config[VERSION_CONSTANT]} = \"{self.new_version}\""
        self._replace_in_file(constant_version_file, to_replace_str, new_str)

    def _update_readme_file(self):
        readme_file = join(self.entry, self.config[README_FILE])
        self._replace_in_file(readme_file, self.previous_version, self.new_version)

    def _replace_in_file(self, file_path, to_replace_old, to_replace_new):
        if isfile(file_path):
            with open(file_path, "r+", encoding="utf-8") as f:
                content = f.read()
                if to_replace_old in content and to_replace_new not in content:
                    content = content.replace(to_replace_old, to_replace_new)
                    f.seek(0)
                    f.write(content)
                    f.truncate()
                    self.updated_files.append(file_path)
                else:
                    self.logger.warning(f"Previous version ({self.previous_version}) not found in {file_path}, "
                                        f"version number can't be updated there. This might be normal if this file "
                                        f"does not contain version in this form or has already been updated.")

        else:
            self.logger.warning(f"No {file_path} found in this repository, version number can't be updated.")

    def sanitize_repo_name(self):
        return self.entry.name.replace(" ", "_").replace("-", "_").lower()

    def __str__(self):
        return self.get_name()
