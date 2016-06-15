import unittest

import click
import mock
from click.testing import CliRunner
from testfixtures import Replacer
from testfixtures.popen import MockPopen

from utils.command import Command, CommandResult


class CommandsTest(unittest.TestCase):

    @mock.patch('utils.command.Command._dollar_split')
    @mock.patch('utils.command.Command._call_cmd')
    def test_call(self, mock_call, mock_split):
        Command.call('cmd1$cmd2')
        mock_split.assert_called_with('cmd1$cmd2')

        Command.call('cmd1')
        mock_call.assert_called_with('cmd1')

    @mock.patch('utils.command.Command.call')
    @mock.patch('click.echo')
    def test_dollar_split(self, mock_echo, mock_call):
        mock_call.side_effect = [
            CommandResult('id1\nid2'),
            CommandResult('main cmd'),
            CommandResult(None),
        ]
        result = Command._dollar_split('cmd1$cmd2')
        mock_echo.assert_called_with('List of ids: id1 id2')
        self.assertEqual(result.output, 'main cmd')

        result = Command._dollar_split('cmd1$cmd2')
        mock_echo.assert_called_with('No ids found.')
        self.assertEqual(result.output, None)

    def test_fmt(self):
        @click.command()
        @click.argument('str_name')
        @click.argument('data')
        def fmt(str_name, data):
            click.echo('=== {} ===\n{}'.format(str_name, data))

        runner = CliRunner()
        result = runner.invoke(fmt, ['Str1', 'some data'])
        assert result.exit_code == 0
        assert '=== Str1 ===\nsome data' in result.output



class PopenCommandsTest(unittest.TestCase):

    def setUp(self):
        self.Popen = MockPopen()
        self.r = Replacer()
        self.r.replace('utils.command.subprocess.Popen', self.Popen)
        self.addCleanup(self.r.restore)

    def test_call_cmd(self):
        self.Popen.set_command('cmd1', stdout='foo')
        command_result = Command._call_cmd('cmd1')
        expected_command_result = CommandResult(output='foo', return_code=0)
        self.assertEqual(command_result.output, expected_command_result.output)
        self.assertEqual(command_result.return_code, expected_command_result.return_code)
        self.assertFalse(command_result.err)