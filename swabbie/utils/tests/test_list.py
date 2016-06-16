import unittest

import mock

from swabbie.utils.list import List, ChangeReport
from swabbie.utils.command import CommandResult


@mock.patch('swabbie.utils.command.Command.call')
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
        mock_command_call.return_value = CommandResult(output='obj1\nobj2')

        output = List.display_list('Test', 'test cmd')
        self.assertEqual(output, "=== Test ===\nobj1\nobj2")

    def test_display_list_none(self, mock_command_call):
        mock_command_call.return_value = CommandResult(output='')

        output = List.display_list('Test', 'test cmd2')
        self.assertEqual(output, 'No test found')

    @mock.patch('swabbie.utils.list.List.get_count')
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