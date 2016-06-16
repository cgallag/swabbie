import unittest

import mock

from swabbie.utils.clean import Clean
from swabbie.utils.list import ChangeReport


class TestClean(unittest.TestCase):

    def test_summary(self):
        change_report = ChangeReport(start=2, end=1)
        summary = Clean._summary(change_report, 'Images')
        self.assertEqual(summary,
                         'Images\n\t1 removed\n\t1 remaining\n')

        change_report = ChangeReport(start=0, end=0)
        summary = Clean._summary(change_report, 'images')
        self.assertEqual(summary,
                         'No images were found.\n')

    @mock.patch('swabbie.utils.list.List.change_report')
    def test_clean(self, mock_change_report):
        mock_change_report.side_effect = [
            ChangeReport(2, 1),
            ChangeReport(4, 2)
        ]

        clean_report = Clean.clean()
        self.assertEqual(clean_report,
                         'Dangling images\n\t1 removed\n\t1 remaining\n' \
                         'Exited containers\n\t2 removed\n\t2 remaining\n')

    @mock.patch('swabbie.utils.list.List.change_report')
    def test_nuke(self, mock_change_report):
        mock_change_report.side_effect = [
            ChangeReport(2, 0),
            ChangeReport(4, 0)
        ]

        nuke_report = Clean.nuke()
        self.assertEqual(nuke_report,
                         'Images\n\t2 removed\n\t0 remaining\n' \
                         'Containers\n\t4 removed\n\t0 remaining\n')