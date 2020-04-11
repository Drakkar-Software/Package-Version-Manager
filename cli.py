#  Drakkar-Software Package-Version-Manager
import argparse
from logging.config import fileConfig
import sys
from os.path import abspath
from yaml import load, FullLoader

from package_version_manager import PROJECT_NAME
from package_version_manager import VERSION
from package_version_manager.constants import DEFAULT_CONFIG_FILE, LOGGING_CONFIG_FILE
from package_version_manager.directory_crawler import DirectoryCrawler


def handle_package_version_manager_command(target_dir, configuration, skip_confirmations=False):
    crawler = DirectoryCrawler(target_dir, configuration, skip_confirmations)
    crawler.find_repos_to_update()
    crawler.update_repos()


def register_arguments(tentacles_parser) -> None:
    tentacles_parser.add_argument("-c", "--config",
                                  help=f"Path to the config file to use. Default is {DEFAULT_CONFIG_FILE}",
                                  type=str,
                                  default=DEFAULT_CONFIG_FILE)
    tentacles_parser.add_argument("-d", "--target-directory",
                                  help="Path to the target directory to process. "
                                                                   "Default is '.'",
                                  type=str,
                                  default=".")
    tentacles_parser.add_argument("-f", "--skip-confirmations",
                                  help="Skip user confirmations.",
                                  action="store_true")


def _load_config(file_name):
    with open(file_name) as config_file:
        return load(config_file, Loader=FullLoader)


if __name__ == "__main__":
    fileConfig(LOGGING_CONFIG_FILE)
    parser = argparse.ArgumentParser(description=f"{PROJECT_NAME} [version: {VERSION}] CLI")
    register_arguments(parser)
    args = parser.parse_args(sys.argv[1:])
    config = _load_config(args.config)
    sys.exit(handle_package_version_manager_command(abspath(args.target_directory), config, args.skip_confirmations))