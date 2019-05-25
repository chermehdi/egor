"""
  Entry point of the command line helper
"""
import sys

from knack import CLI

from egor.commands import EgorCommandHelp, EgorCommandLoader
from egor.config import COMMAND_ENV_PREFIX, COMMAND_NAME, COMMAND_SETTINGS_DIR
from egor.invocation import EgorInvoker


def cli():
    return CLI(
        cli_name=COMMAND_NAME,
        config_dir=COMMAND_SETTINGS_DIR,
        config_env_var_prefix=COMMAND_ENV_PREFIX,
        invocation_cls=EgorInvoker,
        commands_loader_cls=EgorCommandLoader,
        help_cls=EgorCommandHelp
    )


def launch():
    """
    Egor CLI entry point, this is invoked for each usage of the egor command
    """

    arguments = sys.argv[1:]
    cli_env = cli()
    exit_code = cli_env.invoke(args=arguments)

    return exit_code
