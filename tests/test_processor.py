import unittest
from functions.processor import FileProcessor
import tempfile
from unittest.mock import patch, MagicMock

class TestFileProcessor(unittest.TestCase):

    @patch("functions.processor.ValueModifier")
    def test_processing(self, MockValueModifier):
        mock_vm_instance = MockValueModifier.return_value
        mock_vm_instance.get_multiplier.side_effect = lambda instrument: 1.0
        sample_data = (
            "INSTRUMENT1, 20-May-2022, 10.0\n"
            "INSTRUMENT1, 21-May-2022, 20.0\n"
            "INSTRUMENT2, 10-Nov-2024, 30.0\n"
            "INSTRUMENT3, 20-Jun-2024, 40.0\n"
            "d, 22-Jun-2025, 50.0\n"
        )
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_data, \
             tempfile.NamedTemporaryFile(mode="w+", delete=False) as tmp_log:

            tmp_data.write(sample_data)
            tmp_data.flush()

            processor = FileProcessor(tmp_data.name, tmp_log.name)
            processor.process()
            result = processor.results()

        self.assertAlmostEqual(result["mean"], 15.0)
        self.assertAlmostEqual(result["mean_selected_date"], 30.0)
        self.assertAlmostEqual(result["latest_sum"], 50.0)

if __name__ == "__main__":
    unittest.main()
