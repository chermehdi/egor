"""
Task related functions, parsing, compiling and testing tasks
"""
import os
import sys

import pyperclip
from knack.log import get_logger
from pkg_resources import resource_filename

from egor.config import get_configuration_value
from egor.judge import execute_cpp_task, execute_java_task
from egor.meta import MetaDataHandler
from egor.server import start_server
from egor.util import get_current_directory, get_meta_data_path, get_eof_signal_key

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


def parse_task(lang=''):
    """
    This will watch a new event from CHelper extension to create a new task
    :param lang: your source file language
    :return: None
    """
    logger.info('parsing the task ...')
    port = int(get_configuration_value('EGOR_PORT'))
    task_meta = start_server(port)  # todo: find a better solution
    task_file = get_current_directory(task_meta.name, get_file_name(lang))
    logger.info('Generating task file {}'.format(os.path.basename(task_file)))
    with open(task_file, 'w') as task_source:
        task_source.write(task_template_content(lang))

    # add source file data to task metadata
    task_meta.lang = lang
    task_meta.source_file = task_file

    task_meta.persist()


def test_task(name='__current_dir', lang='cpp'):
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

    task_meta = MetaDataHandler(get_meta_data_path(task_dir), exists=True)

    input_files_path = os.path.join(task_dir, 'input')
    output_files_path = os.path.join(task_dir, 'output')
    if not os.path.exists(input_files_path):
        logger.error('There is no input specified for this task, or input directory is missing')
    if not os.path.exists(output_files_path):
        logger.error('There is no output specified for this task, or output directory is missing')

    if lang == 'cpp':
        execute_cpp_task(task_meta)
    elif lang == 'java':
        execute_java_task(task_meta)
    elif lang == 'python':
        # todo: add python support
        pass
    else:
        logger.error('Language specified {} is not yet supported'.format(lang))


def remove_task(name):
    """
    This will simply remove all the files associated with a given task
    """
    print("remove task {name}".format(name=name))


def copy_task(name, lang):
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


def new_test_case(name='__current_dir', with_output=False):
    """
    Prompts the user to enter a new test case
    :param with_output: Determines if the user knows the output of the input in advance or not
    :param name: name of the problem, leave this options if you are currently in the problem's directory
    :return: None
    """
    task_dir = get_current_directory(name)

    if name == '__current_dir':
        task_dir = get_current_directory()

    task_meta = MetaDataHandler(get_meta_data_path(task_dir), exists=True)
    input_dir = os.path.join(task_dir, 'input')

    next_input_file_number = len(task_meta.tests) + 1
    input_file_name = 'in-{}.in'.format(next_input_file_number)
    input_file_path = os.path.join(input_dir, input_file_name)
    print('Enter your input here, press {} to terminate input'.format(get_eof_signal_key()))
    input_file_content = sys.stdin.read()

    test_description = {
        'input_file': input_file_path,
        'output_file': '',
        'index': next_input_file_number,
        'custom': True
    }

    with open(input_file_path, "w", encoding='utf-8') as input_file:
        input_file.write(input_file_content)

    if with_output:
        print('Enter your output here, press {} to terminate input'.format(get_eof_signal_key()))
        output_file_content = sys.stdin.read()
        output_file_path = os.path.join(task_meta.output_dir, 'in-{}-expected.out'.format(next_input_file_number))
        with open(output_file_path, "w", encoding='utf-8') as output_file:
            output_file.write(output_file_content)

        test_description['output_file'] = output_file_path

    task_meta.tests.append(test_description)

    task_meta.persist()

    logger.info('New input file generated successfully')
