"""
Utilities function used across the project
"""
import os
import sys

from egor.config import get_configuration_value


def is_help_command(command) -> bool:
    """
     Checks that the user inputted command is a help command, which will not go over the wire.
      This is a command with -h or --help.
      The help functionality is triggered no matter where the -h appears in the command (arg ordering)
    """
    for part in command:
        if part in ('-h', '--help'):
            return True
    return False


def get_current_directory(*paths) -> str:
    """
    Computes and returns the absolute path to the current directory
    if paths are specified, they are joined with with the current directory path
    """
    cur_dir_path = os.path.abspath(os.path.curdir)
    if len(paths):
        cur_dir_path = os.path.join(cur_dir_path, *paths)

    return cur_dir_path


def extract_test_number_from_filename(file) -> int:
    """
    Extract the number of the test case from the filename/path.
    :param file: filename or path
    :return: the number of the file
    """
    # the parameter could be a path
    file = os.path.basename(file)
    return int(file.split('-')[1].split('.')[0])


def get_default_language():
    return get_configuration_value('EGOR_DEFAULT_LANG', 'cpp')


DIFFERENT_OUTPUT_LENGTH_TEMPLATE = \
    """
    Number of lines of expected output is different from the produced output
    expected {}, found {}
    """
DIFFERENT_OUTPUT_CONTENT_TEMPLATE = \
    """
    Difference in line {}:
    - Expected output:
    {}
    - Produced output:
    {}
    """

PASSED_TEST_CASE = 'Passed test case {}'

SKIPPED_TEST_CASE = 'Skipped test case {}'


def get_last_input_file_number(input_dir) -> int:
    """
    Will get the last input file number in the input directory.
    The function will find all input file numbers and will return the max
    :param input_dir: input directory
    :return: number of last input file
    """
    return max(list(map(extract_test_number_from_filename, os.listdir(input_dir))))


def get_meta_data_path(task_dir) -> str:
    """
    Returns the path to the metadata file path, by just adding 'egor-meta.json' with the current task dir
    :param task_dir: Current task directory
    :return: path to the metadata file
    """
    return os.path.join(task_dir, 'egor-meta.json')


def is_mac_os() -> bool:
    """
    :return: True if is mac os False otherwise
    """
    return sys.platform == 'darwin'


def get_eof_signal_key() -> str:
    """
    Returns the key binding associated to EOF depending on which platform
    Egor is running on
    :return: Key binding description
    """
    return 'Cmd + D' if is_mac_os() else 'Ctrl + D'
