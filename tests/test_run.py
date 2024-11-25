import unittest
from unittest.mock import patch, MagicMock
import sys
import importlib


class TestRun(unittest.TestCase):

    def setUp(self):
        """
        Clear the cached version of `run` module before each test.
        """
        if 'run' in sys.modules:
            del sys.modules['run']

    @patch('sys.argv', ['run.py', '--feature', '0'])
    @patch('run.ExampleAnalysis')
    @patch('run.config.overwrite_from_args')
    def test_feature_0(self, mock_config, mock_example_analysis):
        """
        Test that feature 0 (ExampleAnalysis) is executed correctly.
        """
        try:
            import run
        except SystemExit:
            pass

        mock_example_analysis.return_value.run.assert_called_once()
        mock_config.assert_called_once()

    @patch('sys.argv', ['run.py', '--feature', '1'])
    @patch('run.FirstAnalysis')
    @patch('run.config.overwrite_from_args')
    def test_feature_1(self, mock_config, mock_first_analysis):
        """
        Test that feature 1 (FirstAnalysis) is executed correctly.
        """
        try:
            import run
        except SystemExit:
            pass

        mock_first_analysis.return_value.run.assert_called_once()
        mock_config.assert_called_once()

    @patch('sys.argv', ['run.py', '--feature', '2'])
    @patch('run.Second_analysis')
    @patch('run.config.overwrite_from_args')
    def test_feature_2(self, mock_config, mock_second_analysis):
        """
        Test that feature 2 (Second_analysis) is executed correctly.
        """
        try:
            import run
        except SystemExit:
            pass

        mock_second_analysis.return_value.run.assert_called_once()
        mock_config.assert_called_once()

    @patch('sys.argv', ['run.py'])
    def test_missing_feature(self):
        """
        Test that missing the --feature argument raises an error.
        """
        with self.assertRaises(SystemExit):
            import run

    @patch('sys.argv', ['run.py', '--feature', '99'])
    def test_invalid_feature(self):
        """
        Test that an invalid feature prints an error message.
        """
        with patch('builtins.print') as mock_print:
            try:
                import run
            except SystemExit:
                pass
            mock_print.assert_called_once_with(
                'Need to specify which feature to run with --feature flag.'
            )


if __name__ == '__main__':
    unittest.main()
