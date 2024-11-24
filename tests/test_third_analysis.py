import unittest
from unittest.mock import patch
from datetime import datetime, timedelta
from third_analysis import ThirdFeatureAnalysis
from model import Issue, Event, State


class TestThirdFeatureAnalysis(unittest.TestCase):

    def setUp(self):
        """
        Set up mock data and dependencies for tests.
        """
        # Mock events using dictionaries to match the expected input for Event
        self.event_labeled = {
            'event_type': 'labeled',
            'event_date': (datetime.now() - timedelta(days=10)).isoformat(),
        }
        self.event_assigned = {
            'event_type': 'assigned',
            'event_date': (datetime.now() - timedelta(days=5)).isoformat(),
        }
        self.event_invalid = {
            'event_type': 'labeled',
            'event_date': None,  # Invalid date
        }

        # Mock issues using dictionaries to match the expected input for Issue
        self.issue_closed = Issue({
            'state': 'closed',
            'events': [self.event_labeled, self.event_assigned],
            'created_date': (datetime.now() - timedelta(days=30)).isoformat(),
            'updated_date': (datetime.now() - timedelta(days=2)).isoformat(),
        })

        self.issue_open = Issue({
            'state': 'open',
            'events': [self.event_labeled],
            'created_date': (datetime.now() - timedelta(days=20)).isoformat(),
            'updated_date': None,
        })

        self.issue_no_events = Issue({
            'state': 'closed',
            'events': [],
            'created_date': (datetime.now() - timedelta(days=15)).isoformat(),
            'updated_date': (datetime.now() - timedelta(days=10)).isoformat(),
        })

        self.issue_mismatched_events = Issue({
            'state': 'closed',
            'events': [self.event_labeled, self.event_invalid],  # Mismatched event_dates
            'created_date': (datetime.now() - timedelta(days=25)).isoformat(),
            'updated_date': (datetime.now() - timedelta(days=5)).isoformat(),
        })

        # Mock DataLoader to return the test issues
        self.analysis = ThirdFeatureAnalysis()
        self.analysis.issues = [self.issue_closed, self.issue_open, self.issue_no_events, self.issue_mismatched_events]

    @patch("matplotlib.pyplot.show")  # Mock plt.show to avoid displaying plots during tests
    def test_analyze_event_impact_with_valid_data(self, mock_show):
        """
        Test analysis with valid labeled and assigned events.
        """
        self.analysis.analyze_event_impact_on_resolution_time()
        mock_show.assert_called()  # Ensure plots are displayed

    @patch("matplotlib.pyplot.show")  # Mock plt.show to avoid displaying plots during tests
    def test_analyze_event_impact_with_no_events(self, mock_show):
        """
        Test analysis with issues that have no events.
        """
        self.analysis.issues = [self.issue_no_events]
        self.analysis.analyze_event_impact_on_resolution_time()
        mock_show.assert_not_called()  # No plots should be generated

    @patch("matplotlib.pyplot.show")  # Mock plt.show to avoid displaying plots during tests
    def test_analyze_event_impact_with_mismatched_events(self, mock_show):
        """
        Test analysis with issues having mismatched event_types and event_dates.
        """
        self.analysis.issues = [self.issue_mismatched_events]
        self.analysis.analyze_event_impact_on_resolution_time()
        mock_show.assert_not_called()  # No plots should be generated due to mismatched data

    @patch("matplotlib.pyplot.show")  # Mock plt.show to avoid displaying plots during tests
    def test_analyze_event_impact_with_empty_dataframe(self, mock_show):
        """
        Test behavior when resulting DataFrame for labeled/assigned events is empty.
        """
        self.analysis.issues = [
            Issue({'state': 'closed', 'events': [], 'created_date': (datetime.now() - timedelta(days=20)).isoformat()})
        ]
        self.analysis.analyze_event_impact_on_resolution_time()
        mock_show.assert_not_called()  # No plots should be generated

    @patch("matplotlib.pyplot.show")  # Mock plt.show to avoid displaying plots during tests
    def test_plot_generation_with_valid_data(self, mock_show):
        """
        Test that plots are generated when labeled and assigned data exist.
        """
        self.analysis.analyze_event_impact_on_resolution_time()

        # Mocking plt.show ensures plots are called
        self.assertGreater(mock_show.call_count, 0)

if __name__ == "__main__":
    unittest.main()
