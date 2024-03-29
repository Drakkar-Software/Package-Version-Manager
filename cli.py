#  Drakkar-Software Package-Version-Manager
import argparse
import sys
import os
import pathlib
from logging.config import fileConfig

from yaml import load, FullLoader

from package_version_manager import PROJECT_NAME
from package_version_manager import VERSION
from package_version_manager.constants import DEFAULT_CONFIG_FILE, LOGGING_CONFIG_FILE
from package_version_manager.directory_crawler import DirectoryCrawler


def get_resource_or_file_name(file_name: str):
    package_config = os.path.join(pathlib.Path(__file__).parent.absolute(), file_name)
    if os.path.isfile(package_config):
        return package_config
    return file_name


def handle_package_version_manager_command(target_dir, configuration,
                                           skip_confirmations=False,
                                           skip_requirements_update=False,
                                           skip_new_branch_creation=False):
    crawler = DirectoryCrawler(target_dir, configuration, skip_confirmations, skip_requirements_update)
    crawler.find_repos_to_update()
    crawler.update_repos(skip_new_branch_creation)


def register_arguments(tentacles_parser) -> None:
    tentacles_parser.add_argument("-c", "--config",
                                  help=f"Path to the config file to use. Default is {DEFAULT_CONFIG_FILE}",
                                  type=str,
                                  default=get_resource_or_file_name(DEFAULT_CONFIG_FILE))
    tentacles_parser.add_argument("-d", "--target-directory",
                                  help="Path to the target directory to process. Default is '.'",
                                  type=str,
                                  default=".")
    tentacles_parser.add_argument("-f", "--skip-confirmations",
                                  help="Skip user confirmations.",
                                  action="store_true")
    tentacles_parser.add_argument("-s", "--skip-requirements-update",
                                  help="Skip requirements update.",
                                  action="store_true")
    tentacles_parser.add_argument("-j", "--just-commit-and-push",
                                  help="Do not create a new branch, just commit and push.",
                                  action="store_true")


def _load_config(file_name):
    with open(file_name) as config_file:
        return load(config_file, Loader=FullLoader)


def main():
    fileConfig(get_resource_or_file_name(LOGGING_CONFIG_FILE))
    parser = argparse.ArgumentParser(description=f"{PROJECT_NAME} [version: {VERSION}] CLI")
    register_arguments(parser)
    args = parser.parse_args(sys.argv[1:])
    config = _load_config(args.config)
    sys.exit(handle_package_version_manager_command(os.path.abspath(args.target_directory), config,
                                                    args.skip_confirmations,
                                                    args.skip_requirements_update,
                                                    args.just_commit_and_push))


if __name__ == "__main__":
    main()
