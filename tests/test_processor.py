import unittest
from functions.processor import FileProcessor
import tempfile

class TestFileProcessor(unittest.TestCase):

    def test_processing(self):
        sample_data = (
            "a, 20-May-2022, 10.0\n"
            "a, 21-May-2022, 20.0\n"
            "b, 10-May-2023, 30.0\n"
            "c, 20-Jun-2024, 40.0\n"
            "d, 22-Jun-2025, 50.0\n"
        )
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp:
            tmp.write(sample_data)
            tmp.seek(0)
            processor = FileProcessor(tmp.name)
            processor.process()
            result = processor.results()

        self.assertAlmostEqual(result["mean_a"], 15.0)
        self.assertAlmostEqual(result["mean_b_may_2023"], 30.0)
        self.assertAlmostEqual(result["latest_sum_exclude_a_b"], 90.0)

if __name__ == "__main__":
    unittest.main()