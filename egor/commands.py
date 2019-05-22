from collections import OrderedDict

from knack.arguments import ArgumentsContext
from knack.commands import CLICommandsLoader, CommandGroup
from knack.help import CLIHelp

from egor.config import VERSION
from egor.help import HelpGenerator

# load helps
HelpGenerator().load()


class EgorCommandHelp(CLIHelp):
    """
    Help generator for egor command
    """

    def __init__(self, cli_ctx=None):
        header_message = \
            """
            ______
          / ____/___  _____ _____
         / __/ / __ `/ __ \/ ___/
        / /___/ /_/ / /_/ / /
       /_____/\__, /\____/_/
             /____/            version: {}
      |------------------------------------>>
        
      Commands:
            """.format(VERSION)

        super(EgorCommandHelp, self).__init__(
            cli_ctx=cli_ctx, welcome_message=header_message)


class EgorCommandLoader(CLICommandsLoader):
    """
    Command loader for egor, where all commands and subcommands
    are registred and arguments associated are added
    """

    def __init(self, *args, **kwargs):
        super(EgorCommandLoader, self).__init__(*args, **kwargs)

    def load_command_table(self, args):
        with CommandGroup(self, 'task', 'egor.task#{}') as g:
            g.command('parse', 'parse_task')
            g.command('test', 'test_task')
            g.command('remove', 'remove_task')
            g.command('copy', 'copy_task')
        return OrderedDict(self.command_table)

    def load_arguments(self, command):
        with ArgumentsContext(self, 'task parse') as args_context:
            args_context.argument('lang', type=str, default='cpp')
        with ArgumentsContext(self, 'task teset') as args_context:
            args_context.argument('name', type=str, default='')
        super(EgorCommandLoader, self).load_arguments(command)
