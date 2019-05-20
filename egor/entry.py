"""
  Entry point of the command line helper
"""
import sys
from knack import CLI
from knack.invocation import CommandInvoker
from egor.util import is_help_command
from egor.config import COMMAND_ENV_PREFIX, COMMAND_NAME, COMMAND_SETTINGS_DIR
from egor.commands import EgorCommandHelp, EgorCommandLoader
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
    help_command = is_help_command(arguments)
    exit_code = cli_env.invoke(args=arguments)

    if help_command:
        return 0
