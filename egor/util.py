"""
Utilities function used accross the project
"""


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
