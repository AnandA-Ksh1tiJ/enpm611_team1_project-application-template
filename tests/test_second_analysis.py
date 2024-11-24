import unittest
from unittest.mock import patch, MagicMock
from second_analysis import Second_analysis


class TestSecondAnalysis(unittest.TestCase):

    @patch('second_analysis.config.get_parameter')
    @patch('second_analysis.DataLoader')
    @patch('second_analysis.plt')
    def test_run(self, mock_plt, mock_data_loader, mock_get_parameter):
        mock_get_parameter.return_value = "test_user"

        # Mock issues and events
        mock_event1 = MagicMock()
        mock_event1.event_type = 'commented'
        mock_event1.author = 'user1'

        mock_event2 = MagicMock()
        mock_event2.event_type = 'commented'
        mock_event2.author = 'user2'

        mock_issue = MagicMock()
        mock_issue.events = [mock_event1, mock_event2]

        mock_data_loader.return_value.get_issues.return_value = [mock_issue]

        # Run analysis
        analysis = Second_analysis()
        analysis.run()

        # Verify the bar plot
        mock_plt.bar.assert_called_once()
        mock_plt.show.assert_called_once()

    @patch('second_analysis.DataLoader')
    @patch('second_analysis.plt')
    def test_run_no_data(self, mock_plt, mock_data_loader):
        """
        Test the run method when no issues are returned by the data loader
        """
        # Mock the data loader to return no issues
        mock_data_loader.return_value.get_issues.return_value = []

        # Initialize the analysis object and run the analysis
        analysis = Second_analysis()
        analysis.run()

        # Verify that plt.bar is called with empty data
        mock_plt.bar.assert_called_once_with([], [])
        mock_plt.show.assert_called_once()

    @patch('second_analysis.DataLoader')
    def test_run_different_event_type(self, mock_data_loader):
        """
        Test the run method when events other than 'commented' exist
        """
        # Mock events of different types
        mock_event = MagicMock()
        mock_event.event_type = 'created'
        mock_event.author = 'user1'

        mock_issue = MagicMock()
        mock_issue.events = [mock_event]

        mock_data_loader.return_value.get_issues.return_value = [mock_issue]

        # Run analysis
        analysis = Second_analysis()
        analysis.run()

    @patch('second_analysis.DataLoader')
    @patch('second_analysis.plt')
    def test_run_large_data(self, mock_plt, mock_data_loader):
        """
        Test the run method with a large number of events
        """
        # Mock a large number of events
        mock_events = []
        for i in range(1000):
            mock_event = MagicMock()
            mock_event.event_type = 'commented'
            mock_event.author = f'user{i % 10}'
            mock_events.append(mock_event)

        mock_issue = MagicMock()
        mock_issue.events = mock_events

        mock_data_loader.return_value.get_issues.return_value = [mock_issue]

        # Run analysis
        analysis = Second_analysis()
        analysis.run()

        # Verify the bar plot
        mock_plt.bar.assert_called_once()


if __name__ == '__main__':
    unittest.main()
