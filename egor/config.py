"""
  Config file to store all contestants for the project
"""

import os

from knack.config import CLIConfig

COMMAND_NAME = 'egor'
COMMAND_SETTINGS_DIR = os.path.expanduser(
    os.path.join('~', '.{}'.format(COMMAND_NAME)))
COMMAND_ENV_PREFIX = COMMAND_NAME.upper()
VERSION = '1.0.0'


def get_configuration_value(name, fallback=None):
    """
    Gets a configuration by name, if the configuration name is not found
    the function will return the provided fallback
    """
    cli_configuration = CLIConfig(COMMAND_SETTINGS_DIR, COMMAND_ENV_PREFIX)

    return cli_configuration.get(COMMAND_NAME, name, fallback)


def set_configuration_value(name, value):
    """
    Sets a configuration's value
    """
    cli_configuration = CLIConfig(COMMAND_SETTINGS_DIR, COMMAND_ENV_PREFIX)

    cli_configuration.set_value(COMMAND_NAME, name, value)
