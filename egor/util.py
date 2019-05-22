"""
Utilities function used accross the project
"""
import os

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
