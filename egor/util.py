"""
Utilities function used accross the project
"""
import os


def is_help_command(command):
    """
     Checks that the user inputted command is a help command, which will not go over the wire.
      This is a command with -h or --help.
      The help functionality is triggered no matter where the -h appears in the command (arg ordering)
    """
    for part in command:
        if part in ('-h', '--help'):
            return True
    return False


def get_current_directory(*paths):
    """
    Computes and returns the absolute path to the current directory
    if paths are specified, they are joined with with the current directory path
    """
    cur_dir_path = os.path.abspath(os.path.curdir)
    if len(paths):
        cur_dir_path = os.path.join(cur_dir_path, *paths)

    return cur_dir_path
