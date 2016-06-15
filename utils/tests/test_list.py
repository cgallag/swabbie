import unittest

import mock

from utils.list import List, ChangeReport
from utils.command import CommandResult


@mock.patch('utils.command.Command.call')
class TestList(unittest.TestCase):

    def test_get_count(self, mock_command_call):
        mock_command_call.return_value = CommandResult(output='1\n2\n3')

        count = List.get_count('test')
        self.assertEqual(count, 1)

    def test_get_count_err(self, mock_command_call):
        mock_command_call.return_value = CommandResult(output=None)

        count = List.get_count('test')
        self.assertEqual(count, 'No count available')

    def test_display_list(self, mock_command_call):
        mock_command_call.side_effect = ['obj1\nobj2', '']

        # If objects listed
        output = List.display_list('Test', 'test cmd')
        self.assertEqual(output, "=== Test ===\nobj1\nobj2")

        # If no objects listed
        output = List.display_list('Test', 'test cmd2')
        self.assertEqual(output, '0 test found')

    @mock.patch('utils.list.List.get_count')
    def test_change_report(self, mock_count, mock_command_call):
        mock_count.side_effect = [0, 2, 1]

        # If start count == 0
        change_report = List.change_report('change cmd', 'list cmd')
        self.assertEqual(change_report,
                         ChangeReport())
        self.assertFalse(mock_command_call.called)

        # If start count > 0
        change_report = List.change_report('change cmd', 'list cmd')
        self.assertEqual(change_report,
                         ChangeReport(start=2, end=1))
        self.assertTrue(mock_command_call.called)