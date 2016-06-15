import unittest

import mock

from utils.clean import Clean
from utils.list import ChangeReport


class TestClean(unittest.TestCase):

    def test_summary(self):
        change_report = ChangeReport(start=2, end=1)
        summary = Clean._summary(change_report, 'images')
        self.assertEqual(summary,
                         '1 images removed\n1 images remaining\n')

        change_report = ChangeReport(start=0, end=0)
        summary = Clean._summary(change_report, 'images')
        self.assertEqual(summary,
                         'No images were found.\n')

    @mock.patch('utils.list.List.change_report')
    def test_clean(self, mock_change_report):
        mock_change_report.side_effect = [
            ChangeReport(2, 1),
            ChangeReport(4, 2)
        ]

        clean_report = Clean.clean()
        self.assertEqual(clean_report,
                         '1 dangling images removed\n1 dangling images remaining\n' \
                         '2 exited containers removed\n2 exited containers remaining\n')

    @mock.patch('utils.list.List.change_report')
    def test_nuke(self, mock_change_report):
        mock_change_report.side_effect = [
            ChangeReport(2, 0),
            ChangeReport(4, 0)
        ]

        nuke_report = Clean.nuke()
        self.assertEqual(nuke_report,
                         '2 images removed\n0 images remaining\n' \
                         '4 containers removed\n0 containers remaining\n')