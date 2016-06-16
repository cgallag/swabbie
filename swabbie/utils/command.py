import shlex
import subprocess

import click


class CommandResult(object):
    def __init__(self, output, return_code=None, err=None):
        """
        Store data from running a command
        """
        self.output = output or None
        self.return_code = return_code
        self.err = err


class Command(object):

    @classmethod
    def call(cls, cmd_str, **kwargs):
        """
        Runs single and two-part commands
        """
        # Process multi-part command
        if '$' in cmd_str:
            return cls._dollar_split(cmd_str)
        else:
            return cls._call_cmd(cmd_str, **kwargs)

    @classmethod
    def call_list(cls, cmd_list):
        for cmd in cmd_list:
            cls.call(cmd)

    @classmethod
    def _dollar_split(cls, cmd_str):
        """
        Runs command with one $ in it. Retrieves list of docker object ids,
        then executes command on those ids.
        """
        # Separate commands into id-gathering and main commands
        main_cmd, ids_cmd = cmd_str.split('$')
        ids_cmd = ids_cmd.strip('()')

        # Generate ids
        ids_result = cls.call(ids_cmd, hide_output=True)
        if ids_result.output:
            ids_list = ids_result.output.strip().split()
            ids_string = ' '.join(ids_list)
        else:
            ids_string = ''

        if len(ids_string.strip()) > 0:
            click.echo('List of ids: {}'.format(ids_string))

            # Use ids in main command
            full_cmd = '{} {}'.format(main_cmd.strip(), ids_string)
            main_result = cls.call(full_cmd)
            return main_result
        else:
            # Don't execute main command if no ids were found
            click.echo('No ids found.')
            return CommandResult(None)

    @classmethod
    def _call_cmd(cls, cmd_str, stdin_str=None, hide_output=False):
        """
        Runs docker command via subprocess and returns output
        :param cmd_str: command to run
        :param stdin_str:
        :param hide_output: show command output on the command line
        :return:
        """
        # Split command into list
        cmd_list = shlex.split(cmd_str)
        # Run command
        p = subprocess.Popen(
            cmd_list,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=1)

        output = ''
        for line in iter(p.stdout.readline, b''):
            output += line
            if not hide_output:
                print line,
        p.wait()
        # Return command data
        _, err = p.communicate(stdin_str or '')
        return_code = p.returncode

        # TODO: Turn this into an object
        if output and not hide_output:
            cls._echo_output('Output', output)
        if err:
            cls._echo_output('Error', err)
        return CommandResult(output, return_code=return_code, err=err)

    @classmethod
    def _echo_output(cls, str_name, data):
        """
        Show formatted output on command line
        """
        click.echo('=== {} ===\n{}'.format(str_name, data))
