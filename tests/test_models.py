import unittest
from datetime import datetime
from functions.models import DataRow  # Replace 'your_module' with the actual module name

class TestDataRowParsing(unittest.TestCase):

    def test_valid_line(self):
        line = "A, 01-Jan-2023, 123.45"
        row = DataRow.from_csv_line(line)
        self.assertEqual(row.instrument, "A")
        self.assertEqual(row.date, datetime(2023, 1, 1))
        self.assertAlmostEqual(row.value, 123.45)

    def test_valid_line_with_extra_spaces(self):
        line = "  B ,  15-Feb-2022 ,  10.5 "
        row = DataRow.from_csv_line(line)
        self.assertEqual(row.instrument, "B")
        self.assertEqual(row.date, datetime(2022, 2, 15))
        self.assertEqual(row.value, 10.5)

    def test_invalid_column_count(self):
        line = "A,01-Jan-2023"
        with self.assertRaises(ValueError) as cm:
            DataRow.from_csv_line(line)
        self.assertIn("does not have exactly 3 columns", str(cm.exception))

    def test_invalid_date_format(self):
        line = "A,2023-01-01,100.0"  # wrong format
        with self.assertRaises(ValueError) as cm:
            DataRow.from_csv_line(line)
        self.assertIn("Error parsing line", str(cm.exception))

    def test_invalid_value_format(self):
        line = "A,01-Jan-2023,abc"
        with self.assertRaises(ValueError) as cm:
            DataRow.from_csv_line(line)
        self.assertIn("could not convert string to float", str(cm.exception))

    def test_empty_line(self):
        line = ""
        with self.assertRaises(ValueError) as cm:
            DataRow.from_csv_line(line)
        self.assertIn("does not have exactly 3 columns", str(cm.exception))

if __name__ == "__main__":
    unittest.main()
