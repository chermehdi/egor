from knack.util import CommandResultItem
from knack.invocation import CommandInvoker


class EgorInvoker(CommandInvoker):
    def execute(self, args):
        try:
            return super(EgorInvoker, self).execute(args)
        except TypeError as e:
            from knack.log import get_logger
            logger = get_logger(__name__)
            logger.error('Could not execute egor command')
            return CommandResultItem(None, exit_code=0)
