import unittest
from unittest.mock import patch, mock_open
from datetime import datetime

from functions.utils import is_selected_date, format_results, save_results, handle_output
from functions.config import FILTERS, INSTRUMENTS


class TestUtils(unittest.TestCase):

    def test_is_selected_date_true(self):
        date = datetime(FILTERS["YEAR"], FILTERS["MONTH"], 15)
        self.assertTrue(is_selected_date(date))

    def test_is_selected_date_false(self):
        date = datetime(1999, 1, 1)
        self.assertFalse(is_selected_date(date))

    def test_format_results_output(self):
        results = {
            "mean": 10.1234,
            "mean_selected_date": 5.5678,
            "latest_sum": 99.99,
            "stddev": 1.2345
        }

        output = format_results(results)

        self.assertIn(f"Mean for instrument {INSTRUMENTS['MEAN']}", output)
        self.assertIn(f"{results['mean']:.2f}", output)
        self.assertIn(f"{FILTERS['MONTH']}/{FILTERS['YEAR']}", output)

    @patch("functions.utils.os.makedirs")
    @patch("functions.utils.open", new_callable=mock_open)
    @patch("functions.utils.time.time", return_value=1234567890)
    def test_save_results(self, mock_time, mock_file, mock_makedirs):
        content = "Sample output"
        output_dir = "test_output_dir/"

        save_results(content, output_dir)

        expected_path = f"{output_dir}results_1234567890.txt"

        mock_makedirs.assert_called_once_with(output_dir, exist_ok=True)
        mock_file.assert_called_once_with(expected_path, "w")
        mock_file().write.assert_called_once_with(content)

    @patch("functions.utils.save_results")
    @patch("functions.utils.format_results", return_value="formatted string")
    @patch("builtins.print")
    def test_handle_output(self, mock_print, mock_format, mock_save):
        results = {"mean": 1, "mean_selected_date": 2, "latest_sum": 3, "stddev": 4}
        handle_output(results, "out_dir/")

        mock_format.assert_called_once_with(results)
        mock_print.assert_called_once_with("formatted string")
        mock_save.assert_called_once_with("formatted string", "out_dir/")


if __name__ == "__main__":
    unittest.main()
