import unittest
import os

from egor.util import is_help_command, get_current_directory


class UtilTest(unittest.TestCase):

    def test_should_find_help_command(self):
        self.assertFalse(is_help_command(['a', '--b']))
        self.assertTrue(is_help_command(['a', '-h']))
        self.assertTrue(is_help_command(['a', '--help']))

    def test_should_return_absolute_path_to_current_dir(self):
        directory = get_current_directory()
        self.assertEqual(os.path.abspath(os.path.curdir), directory)

    def test_should_return_absolute_path_for_added_values(self):
        directory = get_current_directory('random', 'directory')
        expected = os.path.join(
            os.path.abspath('.'), 'random', 'directory'
        )
        self.assertEqual(expected, directory)
