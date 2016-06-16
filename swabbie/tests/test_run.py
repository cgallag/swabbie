import unittest

import mock
from click.testing import CliRunner

from swabbie.run import clean, count, nuke, list, ref
from swabbie.utils.list import List


class TestSwabbie(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    @mock.patch('swabbie.run.Clean.clean')
    def test_clean(self, mock_clean):
        mock_clean.return_value = 'test'

        result = self.runner.invoke(clean)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'test\n')

    @mock.patch('swabbie.run.Clean.nuke')
    def test_nuke(self, mock_nuke):
        mock_nuke.return_value = 'test'

        result = self.runner.invoke(nuke)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, 'test\n')

    @mock.patch('swabbie.run.List.get_count')
    def test_count(self, mock_count):
        mock_count.side_effect = [1, 2, 3, 4]

        result = self.runner.invoke(count)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output,
                         "Images\n\tNon-Dangling 1\n\tAll 2\n\n" \
                         "Containers\n\tRunning 3\n\tAll 4\n")
        mock_count.assert_any_call(List.Commands.LIVE_IMAGE)
        mock_count.assert_any_call(List.Commands.ALL_IMAGE)
        mock_count.assert_any_call(List.Commands.LIVE_CONTAINER)
        mock_count.assert_any_call(List.Commands.ALL_CONTAINER)

    @mock.patch('swabbie.run.List.display_list')
    def test_list_all(self, mock_list):
        mock_list.side_effect = [0, 0]
        result = self.runner.invoke(list)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, '0\n0\n')
        self.assertEqual(mock_list.call_args_list,
                         [mock.call('Images', List.Commands.ALL_IMAGE),
                          mock.call('Containers', List.Commands.ALL_CONTAINER)])

    @mock.patch('swabbie.run.List.display_list')
    def test_list_live(self, mock_list):
        mock_list.side_effect = [0, 0]
        result = self.runner.invoke(list, ['--live'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, '0\n0\n')
        self.assertEqual(mock_list.call_args_list,
                         [mock.call('Live Images', List.Commands.LIVE_IMAGE),
                          mock.call('Live Containers', List.Commands.LIVE_CONTAINER)])

    def test_ref(self):
        result = self.runner.invoke(ref)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output,
                         'Run image: docker run -it {} /bin/bash\n' \
                         'Run container: docker exec -it {} bash\n')

        result = self.runner.invoke(ref, ['--n', 'test'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output,
                         'Run image: docker run -it test /bin/bash\n' \
                         'Run container: docker exec -it test bash\n')

        result = self.runner.invoke(ref, ['--c', 'runimg'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output,
                         'Run image: docker run -it {} /bin/bash\n')

        result = self.runner.invoke(ref, ['--c', 'runimg', '--n', 'test'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output,
                         'Run image: docker run -it test /bin/bash\n')

        result = self.runner.invoke(ref, ['--c', 'runcntr'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output,
                         'Run container: docker exec -it {} bash\n')

        result = self.runner.invoke(ref, ['--c', 'runcntr', '--n', 'test'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output,
                         'Run container: docker exec -it test bash\n')