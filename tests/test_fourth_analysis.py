import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime
from fourth_analysis import FourthAnalysis
from model import Issue


class TestFourthAnalysis(unittest.TestCase):
    def setUp(self):
        """
        Set up mock data and dependencies for tests.
        """
        # Create mock issues with different years
        self.issues = [
            Issue({'number': 1, 'created_date': '2020-05-15T08:00:00Z', 'state': 'open'}),
            Issue({'number': 2, 'created_date': '2021-06-20T08:00:00Z', 'state': 'closed'}),
            Issue({'number': 3, 'created_date': '2021-07-10T08:00:00Z', 'state': 'closed'}),
            Issue({'number': 4, 'created_date': '2022-03-05T08:00:00Z', 'state': 'open'}),
            Issue({'number': 5, 'created_date': None, 'state': 'open'}),
        ]

    @patch("data_loader.DataLoader.get_issues", return_value=[])
    @patch("matplotlib.pyplot.show")
    def test_run_no_issues(self, mock_show, mock_get_issues):
        """
        Test behavior when there are no issues to analyze.
        """
        analysis = FourthAnalysis()
        analysis.run()
        mock_show.assert_not_called()

    @patch("data_loader.DataLoader.get_issues", return_value=[])
    @patch("matplotlib.pyplot.show")
    def test_run_empty_dataframe(self, mock_show, mock_get_issues):
        """
        Test behavior when the DataFrame is empty.
        """
        analysis = FourthAnalysis()
        analysis.run()
        mock_show.assert_not_called()

    @patch("data_loader.DataLoader.get_issues")
    @patch("matplotlib.pyplot.show")
    def test_run_with_valid_issues(self, mock_show, mock_get_issues):
        """
        Test behavior with valid issues that have created_date values.
        """
        mock_get_issues.return_value = self.issues
        analysis = FourthAnalysis()
        analysis.run()
        mock_show.assert_called_once()

    @patch("data_loader.DataLoader.get_issues")
    @patch("matplotlib.pyplot.show")
    def test_run_with_missing_dates(self, mock_show, mock_get_issues):
        """
        Test behavior when some issues have missing created_date values.
        """
        mock_get_issues.return_value = self.issues
        analysis = FourthAnalysis()
        analysis.run()
        mock_show.assert_called_once()


if __name__ == "__main__":
    unittest.main()
