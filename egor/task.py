"""
Task related functions, parsing, compiling and testing tasks
"""
import os

import pyperclip
from knack.log import get_logger
from pkg_resources import resource_filename

from egor.config import get_configuration_value
from egor.judge import execute_cpp_task, execute_java_task
from egor.server import start_server
from egor.util import get_current_directory, get_default_language

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


def parse_task(lang=get_default_language()):
    """
    This will watch a new event from CHelper extension to create a new task
    :param lang: your source file language
    :return: None
    """
    print(resource_filename('egor.templates', 'template.java'))

    logger.info('parsing the task ...')
    port = int(get_configuration_value('EGOR_PORT'))
    task_meta = start_server(port)  # todo: find a better solution
    task_file = get_current_directory(task_meta['name'], get_file_name(lang))
    logger.info('Generating task file {}'.format(os.path.basename(task_file)))
    with open(task_file, 'w') as task_source:
        task_source.write(task_template_content(lang))


def test_task(name='__current_dir', lang=get_default_language()):
    """
    This will test an already parsed task, it will compile and run against input files and
    it will print the results
    :param lang: language of your source file
    :param name: Name of the task you want to run
    :return: None
    """
    task_dir = get_current_directory(name)
    if name == '__current_dir':
        task_dir = get_current_directory()

    if not os.path.exists(task_dir):
        logger.error('No task with the given name {}'.format(name))
        return
    input_files_path = os.path.join(task_dir, 'input')
    output_files_path = os.path.join(task_dir, 'output')
    if not os.path.exists(input_files_path):
        logger.error('There is no input specified for this task, or input directory is missing')
    if not os.path.exists(output_files_path):
        logger.error('There is no output specified for this taks, or output directory is missing')

    input_files = os.listdir(input_files_path)
    output_files = os.listdir(output_files_path)

    # make sure every file name has a correspondent output file
    for input_file_name in input_files:
        input_file_parts = input_file_name.split('.')
        expected_output_file_name = input_file_parts[0] + '-expected.out'
        if not (expected_output_file_name in output_files):
            logger.error('could not file corresponding to output file : {}'.format(input_file_name))
            return

    source_filename = os.path.join(task_dir, get_file_name(lang))

    if lang == 'cpp':
        execute_cpp_task(source_filename, task_dir)
    elif lang == 'java':
        execute_java_task(source_filename, task_dir)
    else:
        logger.error('Language specified {} is not yet supported'.format(lang))


def remove_task(name):
    """
    This will simply remove all the files associated with a given task
    """
    print("remove task {name}".format(name=name))


def copy_task(name='__current_dir', lang=get_default_language()):
    """
    Copy task source file to clipboard
    :param name: name of directory of task
    :param lang: language of the source file
    :return: None
    """
    task_dir = get_current_directory(name)
    file_name = get_file_name(lang)

    if name == '__current_dir':
        task_dir = get_current_directory()

    with open(os.path.join(task_dir, file_name), encoding='utf-8') as source_file:
        file_content = source_file.read()
        pyperclip.copy(file_content)
