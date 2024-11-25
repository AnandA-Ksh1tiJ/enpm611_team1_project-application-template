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
        
        
    @patch("data_loader.DataLoader.get_issues")
    @patch("matplotlib.pyplot.show")
    def test_run_all_missing_dates(self, mock_show, mock_get_issues):
        """
        Test behavior when all issues are missing created_date values.
        """
        issues_with_missing_dates = [
            Issue({'number': 1, 'created_date': None, 'state': 'open'}),
            Issue({'number': 2, 'created_date': None, 'state': 'closed'}),
        ]
        mock_get_issues.return_value = issues_with_missing_dates
        analysis = FourthAnalysis()
        analysis.run()
        mock_show.assert_not_called()  # No plot should be shown
        
        
    @patch("data_loader.DataLoader.get_issues")
    @patch("matplotlib.pyplot.show")
    def test_run_issues_same_year(self, mock_show, mock_get_issues):
        """
        Test behavior when all issues were created in the same year.
        """
        issues_same_year = [
            Issue({'number': 1, 'created_date': '2021-01-15T08:00:00Z', 'state': 'open'}),
            Issue({'number': 2, 'created_date': '2021-06-20T08:00:00Z', 'state': 'closed'}),
            Issue({'number': 3, 'created_date': '2021-12-31T08:00:00Z', 'state': 'open'}),
        ]
        mock_get_issues.return_value = issues_same_year
        analysis = FourthAnalysis()
        analysis.run()
        mock_show.assert_called_once()


    @patch("data_loader.DataLoader.get_issues")
    @patch("matplotlib.pyplot.show")
    def test_run_issues_multiple_decades(self, mock_show, mock_get_issues):
        """
        Test behavior when issues span multiple decades.
        """
        issues_multiple_decades = [
            Issue({'number': 1, 'created_date': '1999-12-31T08:00:00Z', 'state': 'closed'}),
            Issue({'number': 2, 'created_date': '2010-05-15T08:00:00Z', 'state': 'open'}),
            Issue({'number': 3, 'created_date': '2050-01-01T08:00:00Z', 'state': 'open'}),
        ]
        mock_get_issues.return_value = issues_multiple_decades
        analysis = FourthAnalysis()
        analysis.run()
        mock_show.assert_called_once()
        
        
    @patch("data_loader.DataLoader.get_issues")
    @patch("matplotlib.pyplot.show")
    def test_run_invalid_date_formats(self, mock_show, mock_get_issues):
        """
        Test behavior when issues contain invalid created_date formats.
        """
        issues_with_invalid_dates = [
            Issue({'number': 1, 'created_date': '2021-13-45T25:61:00Z', 'state': 'open'}),
            Issue({'number': 2, 'created_date': 'invalid-date', 'state': 'closed'}),
        ]
        mock_get_issues.return_value = issues_with_invalid_dates
        analysis = FourthAnalysis()
        analysis.run()
        mock_show.assert_not_called()  # Invalid dates should result in no analysis


    @patch("data_loader.DataLoader.get_issues")
    @patch("matplotlib.pyplot.show")
    def test_run_mixed_states(self, mock_show, mock_get_issues):
        """
        Test behavior with a mix of open and closed issues.
        """
        mixed_state_issues = [
            Issue({'number': 1, 'created_date': '2020-01-10T08:00:00Z', 'state': 'open'}),
            Issue({'number': 2, 'created_date': '2021-05-15T08:00:00Z', 'state': 'closed'}),
            Issue({'number': 3, 'created_date': '2022-03-20T08:00:00Z', 'state': 'open'}),
        ]
        mock_get_issues.return_value = mixed_state_issues
        analysis = FourthAnalysis()
        analysis.run()
        mock_show.assert_called_once()


    @patch("data_loader.DataLoader.get_issues")
    @patch("matplotlib.pyplot.show")
    def test_run_large_dataset(self, mock_show, mock_get_issues):
        """
        Test behavior when analyzing a very large dataset.
        """
        large_issues = [
            Issue({'number': i, 'created_date': f'2021-01-{i % 31 + 1:02d}T08:00:00Z', 'state': 'closed'})
            for i in range(1, 10001)
        ]
        mock_get_issues.return_value = large_issues
        analysis = FourthAnalysis()
        analysis.run()
        mock_show.assert_called_once()  # Ensure plotting works with large datasets

        
    @patch("data_loader.DataLoader.get_issues")
    @patch("matplotlib.pyplot.show")
    def test_run_single_issue(self, mock_show, mock_get_issues):
        """
        Test behavior when analyzing a single issue.
        """
        single_issue = [
            Issue({'number': 1, 'created_date': '2023-01-01T08:00:00Z', 'state': 'closed'}),
        ]
        mock_get_issues.return_value = single_issue
        analysis = FourthAnalysis()
        analysis.run()
        mock_show.assert_called_once()
        
        
    @patch("data_loader.DataLoader.get_issues")
    @patch("matplotlib.pyplot.show")
    def test_run_issues_in_future(self, mock_show, mock_get_issues):
        """
        Test behavior when all issues have future created_date values.
        """
        future_issues = [
            Issue({'number': 1, 'created_date': '2030-01-01T08:00:00Z', 'state': 'closed'}),
            Issue({'number': 2, 'created_date': '2031-05-10T08:00:00Z', 'state': 'open'}),
        ]
        mock_get_issues.return_value = future_issues
        analysis = FourthAnalysis()
        analysis.run()
        mock_show.assert_not_called()  # No plot for future issues


if __name__ == "__main__":
    unittest.main()
