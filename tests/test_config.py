import unittest
import os
import json
from unittest.mock import patch, mock_open
import config

class TestConfig(unittest.TestCase):

    def setUp(self):
        self.default_config = {"test_param": "test_value"}
        config._config = None  # Reset the global config before each test

    def tearDown(self):
        config._config = None
        for key in list(os.environ.keys()):
            if key.startswith("test_"):
                del os.environ[key]

    @patch('os.getcwd', return_value='/mock/path')
    @patch('os.path.isfile', side_effect=lambda x: x.endswith("config.json"))
    @patch('builtins.open', new_callable=mock_open, read_data='{"test_param": "test_value"}')
    def test_init_config_with_valid_path(self, mock_open, mock_isfile, mock_getcwd):
        config._init_config()
        self.assertEqual(config._config, self.default_config)

    @patch('os.getcwd', return_value='/mock/path')
    @patch('os.path.isfile', return_value=False)
    def test_init_config_without_file(self, mock_isfile, mock_getcwd):
        config._init_config()
        self.assertEqual(config._config, {})

    @patch('config._init_config', side_effect=lambda: setattr(config, '_config', {"test_param": "test_value"}))
    def test_get_parameter_default(self, mock_init_config):
        value = config.get_parameter("nonexistent_param", default="default_value")
        self.assertEqual(value, "default_value")

    @patch('config._init_config', side_effect=lambda: setattr(config, '_config', {}))
    def test_get_parameter_not_found(self, mock_init_config):
        value = config.get_parameter("nonexistent_param")
        self.assertIsNone(value)

    @patch('config.set_parameter')
    def test_overwrite_from_args(self, mock_set_parameter):
        """
        Test overwrite_from_args correctly sets parameters.
        """
        # Use a dictionary to simulate command-line arguments
        class MockArgs:
            def __init__(self):
                self.test_param = "new_value"
                self.none_param = None

        args = MockArgs()
        config.overwrite_from_args(args)

        # Assert that set_parameter was called with the correct arguments
        mock_set_parameter.assert_any_call("test_param", "new_value")


if __name__ == "__main__":
    unittest.main()
