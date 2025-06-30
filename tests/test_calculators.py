import unittest
from datetime import datetime, timedelta
from math import isclose
from functions.calculators import MeanCalculator, LatestSumCalculator, MeanStdDevCalculator

class DataRow:
    def __init__(self, instrument, date, value):
        self.instrument = instrument
        self.date = date
        self.value = value

class TestCalculators(unittest.TestCase):

    def test_mean_calculator_basic(self):
        mc = MeanCalculator("A")
        rows = [
            DataRow("A", datetime(2020,1,1), 10),
            DataRow("A", datetime(2020,1,2), 20),
            DataRow("B", datetime(2020,1,3), 30),
        ]
        for row in rows:
            mc.process(row)
        self.assertEqual(mc.count, 2)
        self.assertAlmostEqual(mc.mean_result(), 15.0)

    def test_mean_calculator_with_date_filter(self):
        def date_filter(date):
            return date.month == 1 and date.year == 2020
        mc = MeanCalculator("A", date_filter=date_filter)
        rows = [
            DataRow("A", datetime(2020,1,1), 10),
            DataRow("A", datetime(2020,2,1), 20),
            DataRow("A", datetime(2020,1,3), 30),
        ]
        for row in rows:
            mc.process(row)
        self.assertEqual(mc.count, 2)
        self.assertAlmostEqual(mc.mean_result(), 20.0)

    def test_mean_calculator_with_invalid_date(self):
        mc = MeanCalculator("A")
        with self.assertRaises(AttributeError):
            mc = MeanCalculator("A", date_filter=lambda d: d.month == 1)
            mc.process(DataRow("A", None, 10))

    def test_latest_sum_calculator_basic(self):
        exclude = {"X", "Y"}
        calc = LatestSumCalculator(exclude_instruments=exclude, top_n=3)
        rows = [
            DataRow("A", datetime(2023, 1, 12), 10),
            DataRow("B", datetime(2023, 1, 8), 20),
            DataRow("X", datetime(2023, 3, 1), 30),
            DataRow("C", datetime(2023, 1, 31), 40),
            DataRow("D", datetime(2023, 2, 1), 50),
        ]
        for row in rows:
            calc.process(row)
        self.assertEqual(calc.sum_result(), 100)

    def test_latest_sum_calculator_with_invalid_date(self):
        calc = LatestSumCalculator(exclude_instruments=set(), top_n=2)
        with self.assertRaises(AttributeError):
            calc.process(DataRow("A", "not-a-date", 10))

    def test_mean_stddev_calculator_basic(self):
        calc = MeanStdDevCalculator("A")
        rows = [
            DataRow("A", datetime.now(), 2.0),
            DataRow("A", datetime.now(), 4.0),
            DataRow("A", datetime.now(), 4.0),
            DataRow("A", datetime.now(), 4.0),
            DataRow("A", datetime.now(), 5.0),
            DataRow("A", datetime.now(), 5.0),
            DataRow("A", datetime.now(), 7.0),
            DataRow("A", datetime.now(), 9.0),
            DataRow("B", datetime.now(), 100.0),
        ]
        for row in rows:
            calc.process(row)
        self.assertAlmostEqual(calc.mean_result(), 5.0)
        expected_stddev = 2.138
        self.assertTrue(isclose(calc.stddev_result(), expected_stddev, rel_tol=1e-3))

    def test_mean_stddev_calculator_with_one_value(self):
        calc = MeanStdDevCalculator("A")
        calc.process(DataRow("A", datetime.now(), 10.0))
        self.assertEqual(calc.mean_result(), 10.0)
        self.assertEqual(calc.stddev_result(), 0.0)

    def test_mean_stddev_calculator_no_values(self):
        calc = MeanStdDevCalculator("A")
        self.assertEqual(calc.mean_result(), 0.0)
        self.assertEqual(calc.stddev_result(), 0.0)

    def test_mean_stddev_calculator_with_non_numeric_value(self):
        calc = MeanStdDevCalculator("A")
        with self.assertRaises(TypeError):
            calc.process(DataRow("A", datetime.now(), "not-a-number"))

    def test_latest_sum_calculator_top_n_zero(self):
        calc = LatestSumCalculator(exclude_instruments=set(), top_n=0)
        calc.process(DataRow("A", datetime.now(), 100))
        self.assertEqual(calc.sum_result(), 0)

if __name__ == "__main__":
    unittest.main()
