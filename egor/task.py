"""
Task related functions, parsing, compiling and testing tasks
"""
from knack.log import get_logger
from egor.config import get_configuration_value

logger = get_logger(__name__)


def parse_task():
    """
    This will watch a new event from CHelper extension to create a new task
    """
    logger.info('parsing the task ...')
    port = get_configuration_value('EGOR_PORT')


def test_task(name):
    """
    This will test an already parsed task, it will compile and run against input files and
    it will print the results
    """
    print("test task {name}".format(name=name))


def remove_task(name):
    """
    This will simply remove all the files associated with a given task
    """
    print("remove task {name}".format(name=name))
