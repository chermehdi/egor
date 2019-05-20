"""
Task related functions, parsing, compiling and testing tasks
"""
from knack.log import get_logger
from egor.config import get_configuration_value
from egor.server import start_server
from egor.util import get_current_directory
from pkg_resources import resource_filename
import os

logger = get_logger(__name__)


def get_file_name(lang):
    if lang == 'cpp':
        return 'main.cpp'
    if lang == 'java':
        return 'Main.java'
    if lang == 'py':
        return 'main.py'


def task_template_content(lang):
    if lang == 'py':
        return ''
    task_template = resource_filename(
        'egor.templates', 'template.{}'.format(lang))
    with open(task_template, 'r') as file_template:
        return file_template.read()


def parse_task(lang='cpp'):
    """
    This will watch a new event from CHelper extension to create a new task
    """
    print(resource_filename('egor.templates', 'template.java'))

    logger.info('parsing the task ...')
    port = int(get_configuration_value('EGOR_PORT'))
    task_meta = start_server(port)  # todo: find a better solution
    task_file = get_current_directory(task_meta['name'], get_file_name(lang))
    logger.info('Generating task file {}'.format(os.path.basename(task_file)))
    with open(task_file, 'w') as task_source:
        task_source.write(task_template_content(lang))


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
