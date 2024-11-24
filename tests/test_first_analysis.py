import unittest
from unittest.mock import patch, MagicMock
from first_analysis import FirstAnalysis
from model import Issue, Event


class TestFirstAnalysis(unittest.TestCase):
    def setUp(self):
        # Mock data setup for issues and events
        self.mock_issues = [
            Issue({
                "url": "http://example.com/issue/1",
                "creator": "creator1",
                "labels": ["bug"],
                "state": "open",
                "assignees": ["dev1"],
                "title": "Test Issue 1",
                "text": "Issue description 1",
                "number": 1,
                "created_date": "2024-01-01T00:00:00Z",
                "updated_date": "2024-01-02T00:00:00Z",
                "timeline_url": "http://example.com/timeline/1",
                "events": [
                    {"event_type": "comment", "author": "Alice", "event_date": "2024-01-01T12:00:00Z"},
                    {"event_type": "comment", "author": "Oscar", "event_date": "2024-01-01T13:00:00Z"}
                ]
            }),
            Issue({
                "url": "http://example.com/issue/2",
                "creator": "creator2",
                "labels": ["feature"],
                "state": "closed",
                "assignees": ["dev2"],
                "title": "Test Issue 2",
                "text": "Issue description 2",
                "number": 2,
                "created_date": "2024-01-03T00:00:00Z",
                "updated_date": "2024-01-04T00:00:00Z",
                "timeline_url": "http://example.com/timeline/2",
                "events": [
                    {"event_type": "review", "author": "Henry", "event_date": "2024-01-03T12:00:00Z"},
                    {"event_type": "comment", "author": "Zara", "event_date": "2024-01-03T13:00:00Z"}
                ]
            })
        ]

    @patch('data_loader.DataLoader.get_issues')
    def test_grouped_keys_categorization(self, mock_get_issues):
        """
        Test the grouping and categorization of keys based on alphabetical ranges
        as performed in the original `run` function.
        """
        # Mock the issues loaded by DataLoader
        mock_get_issues.return_value = self.mock_issues

        # Create an instance of FirstAnalysis
        analysis = FirstAnalysis()

        # Mock the print and input calls
        with patch('builtins.print') as mock_print:
            # Simulate user inputs: select A-G and then select Alice
            with patch('builtins.input', side_effect=[1, "1"]):  
                analysis.run()

                # Check that the correct grouping was displayed
                mock_print.assert_any_call("Please select an alphabetical range of author usernames to view:")
                mock_print.assert_any_call("1. A-G")
                mock_print.assert_any_call("2. H-N")
                mock_print.assert_any_call("3. O-T")
                mock_print.assert_any_call("4. U-Z")

                # Verify grouping and categorization behavior
                # Check that "Alice" (A-G) is categorized correctly
                mock_print.assert_any_call("\nCategory: A-G")
                mock_print.assert_any_call(f"{'1':<3} | {'Alice':<5} | {1:>5}")

                # Verify user selection of author
                mock_print.assert_any_call("Event Author found: ", "Alice")

    @patch('data_loader.DataLoader.get_issues')
    def test_user_author_selection(self, mock_get_issues):
        """
        Test user interaction for selecting an author and verifying results.
        """
        mock_get_issues.return_value = self.mock_issues

        analysis = FirstAnalysis()

        # Simulate mock issues loaded by DataLoader
        with patch('builtins.input', side_effect=[1, "1"]):  # Select 'A-G', then select Alice (index 1)
            with patch('builtins.print') as mock_print:
                analysis.run()

                # Check the output for selected author
                mock_print.assert_any_call("Event Author found: ", "Alice")

    @patch('data_loader.DataLoader.get_issues')
    def test_invalid_user_choice(self, mock_get_issues):
        """
        Test handling of invalid user inputs for the alphabetical range selection.
        """
        mock_get_issues.return_value = self.mock_issues

        analysis = FirstAnalysis()

        # Simulate user inputs: invalid choice, then valid choice
        with patch('builtins.input', side_effect=["5", 1, "1"]):  # Invalid, then valid choices
            with patch('builtins.print') as mock_print:
                analysis.run()

                # Verify error message for invalid input
                mock_print.assert_any_call("Invalid choice. Please select a number between 1 and 4.")
                mock_print.assert_any_call("Event Author found: ", "Alice")
    
    @patch('data_loader.DataLoader.get_issues')
    def test_invalid_name_and_valid_name_selection(self, mock_get_issues):
        """
        Test handling of invalid name input followed by a valid name input.
        """
        mock_get_issues.return_value = self.mock_issues

        analysis = FirstAnalysis()

        # Simulate valid category selection, invalid name, then valid name
        with patch('builtins.input', side_effect=["1", "InvalidName", "Alice"]):  # Select category A-G, then invalid name, then valid name
            with patch('builtins.print') as mock_print:
                analysis.run()

                # Verify correct handling of invalid name
                mock_print.assert_any_call("Author not found in the selected category.")

                # Verify correct selection of a valid name
                mock_print.assert_any_call("Event Author found: ", "Alice")


    @patch('data_loader.DataLoader.get_issues')
    def test_non_integer_input_handling(self, mock_get_issues):
        """
        Test handling of non-integer input that raises a ValueError.
        """
        mock_get_issues.return_value = self.mock_issues

        analysis = FirstAnalysis()

        # Simulate valid category selection, followed by non-integer input, then valid author index
        with patch('builtins.input', side_effect=["1", "NonIntegerInput", "1"]):  # Valid category, non-integer input, then valid index
            with patch('builtins.print') as mock_print:
                analysis.run()

                # Verify handling of non-integer input
                mock_print.assert_any_call("Author not found in the selected category.")

                # Verify valid index selection
                mock_print.assert_any_call("Event Author found: ", "Alice")

if __name__ == '__main__':
    unittest.main()
