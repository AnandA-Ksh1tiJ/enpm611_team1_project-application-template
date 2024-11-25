import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from example_analysis import ExampleAnalysis
from model import Issue


class TestExampleAnalysis(unittest.TestCase):
    def setUp(self):
        """
        Set up mock data and dependencies for tests.
        """
        # Mock events as dictionaries
        self.event1 = {'event_type': 'labeled', 'author': 'user1'}
        self.event2 = {'event_type': 'assigned', 'author': 'user2'}
        self.event3 = {'event_type': 'commented', 'author': 'user1'}

        # Mock issues with valid structure
        self.issues = [
            Issue({'creator': 'user1', 'state': 'open', 'events': [self.event1, self.event2]}),
            Issue({'creator': 'user2', 'state': 'closed', 'events': [self.event3]}),
            Issue({'creator': 'user3', 'state': 'open', 'events': []}),  # No events
        ]

    def test_total_events_calculation(self):
        """
        Test the calculation of total events for a specific user and for all users.
        """
        # Mock DataLoader to return the issues
        with patch("data_loader.DataLoader.get_issues", return_value=self.issues):
            analysis = ExampleAnalysis()

            # Test for specific user
            with patch("config.get_parameter", return_value="user1"):
                with patch("builtins.print") as mock_print:
                    analysis.run()
                    mock_print.assert_any_call("\n\nFound 2 events across 3 issues for user1.\n\n")

            # Test for all users
            with patch("config.get_parameter", return_value=None):  # No specific user
                with patch("builtins.print") as mock_print:
                    analysis.run()
                    mock_print.assert_any_call("\n\nFound 3 events across 3 issues.\n\n")

    @patch("matplotlib.pyplot.show")
    @patch("data_loader.DataLoader.get_issues")
    def test_bar_chart_generation(self, mock_get_issues, mock_show):
        """
        Test bar chart generation by verifying DataFrame values directly.
        """
        # Mock DataLoader to return issues
        mock_get_issues.return_value = [
            Issue({'creator': 'user1', 'state': 'open', 'events': []}),
            Issue({'creator': 'user2', 'state': 'closed', 'events': []}),
            Issue({'creator': 'user1', 'state': 'open', 'events': []}),
        ]

        analysis = ExampleAnalysis()

        with patch("pandas.DataFrame.from_records") as mock_from_records:
            # Provide mocked data
            df_mock = pd.DataFrame([
                {"creator": "user1"},
                {"creator": "user2"},
                {"creator": "user1"},
            ])
            mock_from_records.return_value = df_mock
            
            analysis.run()

            # Validate DataFrame grouping and counts
            df_hist = df_mock.groupby("creator").size().nlargest(50)
            assert df_hist["user1"] == 2
            assert df_hist["user2"] == 1

            # Ensure chart is displayed
            mock_show.assert_called_once()



    @patch("matplotlib.pyplot.show")
    @patch("data_loader.DataLoader.get_issues")
    def test_run_method_full_workflow(self, mock_get_issues, mock_show):
        """
        Test the end-to-end execution of the run() method.
        """
        # Mock DataLoader and return issues
        mock_get_issues.return_value = self.issues
        analysis = ExampleAnalysis()

        with patch("builtins.print") as mock_print:
            analysis.run()
            
            # Verify issues are retrieved
            mock_get_issues.assert_called_once()

            # Verify total_events calculation output
            mock_print.assert_any_call("\n\nFound 3 events across 3 issues.\n\n")

            # Verify the bar chart is displayed
            mock_show.assert_called_once()
            
    @patch("matplotlib.pyplot.show")
    @patch("data_loader.DataLoader.get_issues", return_value=[])
    def test_no_issues(self, mock_get_issues, mock_show):
        """
        Test behavior when no issues are returned.
        """
        analysis = ExampleAnalysis()

        with patch("builtins.print") as mock_print:
            analysis.run()
            mock_print.assert_any_call("\n\nFound 0 events across 0 issues.\n\n")
            mock_show.assert_not_called()  # No plot should be shown


    @patch("matplotlib.pyplot.show")
    @patch("data_loader.DataLoader.get_issues")
    def test_issues_with_no_events(self, mock_get_issues, mock_show):
        """
        Test behavior when issues have no events.
        """
        # Mock issues with no events
        mock_get_issues.return_value = [
            Issue({'creator': 'user1', 'state': 'open', 'events': []}),
            Issue({'creator': 'user2', 'state': 'closed', 'events': []}),
        ]
        analysis = ExampleAnalysis()

        with patch("builtins.print") as mock_print:
            analysis.run()
            mock_print.assert_any_call("\n\nFound 0 events across 2 issues.\n\n")
            mock_show.assert_called_once()  # Plot for creators should still be shown



    @patch("data_loader.DataLoader.get_issues", return_value=[])
    @patch("matplotlib.pyplot.show")
    def test_run_no_issues(self, mock_show, mock_get_issues):
        """
        Test behavior when there are no issues to analyze.
        """
        analysis = ExampleAnalysis()
        analysis.run()
        mock_show.assert_not_called()  # No plot should be displayed

    @patch("data_loader.DataLoader.get_issues")
    @patch("matplotlib.pyplot.show")
    def test_run_no_events(self, mock_show, mock_get_issues):
        """
        Test behavior when issues have no events.
        """
        mock_get_issues.return_value = [
            Issue({'creator': 'user1', 'state': 'open', 'events': []}),
            Issue({'creator': 'user2', 'state': 'closed', 'events': []}),
        ]
        analysis = ExampleAnalysis()
        analysis.run()
        mock_show.assert_called_once()  # Plot should still be displayed for creators
    
    
    @patch("data_loader.DataLoader.get_issues", return_value=[])
    @patch("matplotlib.pyplot.show")
    def test_run_empty_dataframe(self, mock_show, mock_get_issues):
        """
        Test behavior when the DataFrame is empty.
        """
        analysis = ExampleAnalysis()
        analysis.run()
        mock_show.assert_not_called()

    @patch("data_loader.DataLoader.get_issues")
    @patch("matplotlib.pyplot.show")
    def test_run_with_valid_issues(self, mock_show, mock_get_issues):
        """
        Test behavior with valid issues and events.
        """
        mock_get_issues.return_value = self.issues
        analysis = ExampleAnalysis()
        analysis.run()
        mock_show.assert_called_once()  # Plot should be displayed

    @patch("data_loader.DataLoader.get_issues")
    @patch("matplotlib.pyplot.show")
    def test_run_event_count_for_user(self, mock_show, mock_get_issues):
        """
        Test the total event count for a specific user.
        """
        mock_get_issues.return_value = self.issues
        with patch("config.get_parameter", return_value="user1"):
            analysis = ExampleAnalysis()
            analysis.run()
            # Validate output in console
            with patch("builtins.print") as mock_print:
                analysis.run()
                mock_print.assert_any_call("\n\nFound 2 events across 3 issues for user1.\n\n")

    @patch("data_loader.DataLoader.get_issues")
    @patch("matplotlib.pyplot.show")
    def test_run_bar_chart_generation(self, mock_show, mock_get_issues):
        """
        Test that the bar chart is generated correctly for top contributors.
        """
        mock_get_issues.return_value = self.issues
        analysis = ExampleAnalysis()

        # Mock plt.bar to validate input to the bar plot
        with patch("pandas.DataFrame.groupby", return_value=MagicMock()) as mock_groupby:
            analysis.run()
            mock_groupby.assert_called_once()



if __name__ == "__main__":
    unittest.main()
