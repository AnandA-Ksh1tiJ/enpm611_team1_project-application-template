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
        
        
    @patch("matplotlib.pyplot.show")  # Mock plt.show to avoid displaying plots during tests
    def test_analyze_event_impact_with_future_event_dates(self, mock_show):
        """
        Test analysis when some events have future event dates.
        """
        future_event = {
            'event_type': 'labeled',
            'event_date': (datetime.now() + timedelta(days=5)).isoformat(),  # Future date
        }
        self.analysis.issues = [
            Issue({
                'state': 'closed',
                'events': [future_event],
                'created_date': (datetime.now() - timedelta(days=30)).isoformat(),
                'updated_date': (datetime.now() - timedelta(days=2)).isoformat(),
            })
        ]
        self.analysis.analyze_event_impact_on_resolution_time()
        mock_show.assert_not_called()  # No plots should be generated due to invalid future dates


    @patch("matplotlib.pyplot.show")  # Mock plt.show to avoid displaying plots during tests
    def test_analyze_event_impact_with_duplicate_events(self, mock_show):
        """
        Test analysis when an issue contains duplicate events.
        """
        self.event_duplicate_1 = {
            'event_type': 'labeled',
            'event_date': (datetime.now() - timedelta(days=10)).isoformat(),
        }
        self.event_duplicate_2 = {
            'event_type': 'labeled',
            'event_date': (datetime.now() - timedelta(days=10)).isoformat(),
        }
                # Pass dictionaries instead of `Event` instances to `events` field
        self.issue_with_duplicates = Issue({
            'state': 'closed',
            'events': [self.event_duplicate_1, self.event_duplicate_2],  # Pass raw data
            'created_date': (datetime.now() - timedelta(days=30)).isoformat(),
            'updated_date': (datetime.now() - timedelta(days=2)).isoformat(),
        })
        
        self.analysis.issues = [self.issue_with_duplicates]
        self.analysis.analyze_event_impact_on_resolution_time()
        mock_show.assert_called_once()  # Plot should be generated but duplicates should be handled


    @patch("matplotlib.pyplot.show")  # Mock plt.show to avoid displaying plots during tests
    def test_analyze_event_impact_with_mixed_states(self, mock_show):
        """
        Test analysis when issues have mixed states (open and closed).
        """
        mixed_state_issues = [
            Issue({
                'state': 'closed',
                'events': [self.event_labeled],
                'created_date': (datetime.now() - timedelta(days=20)).isoformat(),
                'updated_date': (datetime.now() - timedelta(days=5)).isoformat(),
            }),
            Issue({
                'state': 'open',  # Open issue
                'events': [self.event_assigned],
                'created_date': (datetime.now() - timedelta(days=25)).isoformat(),
                'updated_date': None,
            }),
        ]
        self.analysis.issues = mixed_state_issues
        self.analysis.analyze_event_impact_on_resolution_time()
        mock_show.assert_called_once()  # Only closed issues should be analyzed


    @patch("matplotlib.pyplot.show")  # Mock plt.show to avoid displaying plots during tests
    def test_analyze_event_impact_with_empty_issues_list(self, mock_show):
        """
        Test behavior when there are no issues in the dataset.
        """
        self.analysis.issues = []  # No issues at all
        self.analysis.analyze_event_impact_on_resolution_time()
        mock_show.assert_not_called()  # No plots should be generated


    @patch("matplotlib.pyplot.show")  # Mock plt.show to avoid displaying plots during tests
    def test_analyze_event_impact_with_missing_created_date(self, mock_show):
        """
        Test analysis when an issue has a missing created_date.
        """
        issue_missing_created_date = Issue({
            'state': 'closed',
            'events': [self.event_labeled],
            'created_date': None,  # Missing created_date
            'updated_date': (datetime.now() - timedelta(days=5)).isoformat(),
        })
        self.analysis.issues = [issue_missing_created_date]
        self.analysis.analyze_event_impact_on_resolution_time()
        mock_show.assert_not_called()  # No plots should be generated due to missing created_date


    @patch("matplotlib.pyplot.show")  # Mock plt.show to avoid displaying plots during tests
    def test_analyze_event_impact_with_various_event_types(self, mock_show):
        """
        Test analysis when events include unrecognized or unexpected event types.
        """
        unexpected_event = {
            'event_type': 'merged',  # Unrecognized event type
            'event_date': (datetime.now() - timedelta(days=15)).isoformat(),
        }
        self.analysis.issues = [
            Issue({
                'state': 'closed',
                'events': [self.event_labeled, unexpected_event],
                'created_date': (datetime.now() - timedelta(days=30)).isoformat(),
                'updated_date': (datetime.now() - timedelta(days=2)).isoformat(),
            })
        ]
        self.analysis.analyze_event_impact_on_resolution_time()
        mock_show.assert_called_once()  # Only valid event types should be considered



if __name__ == "__main__":
    unittest.main()
