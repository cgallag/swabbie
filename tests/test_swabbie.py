import unittest

import mock
from click.testing import CliRunner

from swabbie import clean, count, nuke, list, ref
from utils.list import List


class TestSwabbie(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    @mock.patch('swabbie.Clean.clean')
    def test_clean(self, mock_clean):
        self.assertFalse(mock_clean.called)

        result = self.runner.invoke(clean)
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(mock_clean.called)

    @mock.patch('swabbie.Clean.nuke')
    def test_nuke(self, mock_nuke):
        self.assertFalse(mock_nuke.called)

        result = self.runner.invoke(nuke)
        self.assertEqual(result.exit_code, 0)
        self.assertTrue(mock_nuke.called)

    @mock.patch('swabbie.List.get_count')
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

    @mock.patch('swabbie.List.display_list')
    def test_list_all(self, mock_list):
        mock_list.side_effect = [0, 0]
        result = self.runner.invoke(list)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, '0\n0\n')
        mock_list.assert_any_call('Images', List.Commands.ALL_IMAGE)
        mock_list.assert_any_call('Containers', List.Commands.ALL_CONTAINER)
        self.assertFalse(mock_list.assert_any_call('Live Images', List.Commands.LIVE_IMAGE))

    @mock.patch('swabbie.List.display_list')
    def test_list_live(self, mock_list):
        mock_list.side_effect = [0, 0]
        result = self.runner.invoke(list, ['--live'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output, '0\n0\n')
        mock_list.assert_any_call('Live Images', List.Commands.LIVE_IMAGE)
        mock_list.assert_any_call('Live Containers', List.Commands.LIVE_IMAGE)
        self.assertFalse(mock_list.assert_any_call('Images', List.Commands.ALL_IMAGE))

    def test_ref(self):
        result = self.runner.invoke(ref)
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output,
                         'Run image: docker run -it {} /bin/bash\n' \
                         'Run container: docker exec -it {} bash\n')

        result = self.runner.invoke(ref, ['--c', 'runimg'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output,
                         'Run image: docker run -it {} /bin/bash\n')

        result = self.runner.invoke(ref, ['--c', 'runcntr'])
        self.assertEqual(result.exit_code, 0)
        self.assertEqual(result.output,
                         'Run container: docker exec -it {} bash\n')