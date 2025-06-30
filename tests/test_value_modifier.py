import unittest
from unittest.mock import patch, MagicMock
from functions.value_modifier import ValueModifier


class TestValueModifier(unittest.TestCase):
    def setUp(self):
        self.db_path = "fake_db_path.db"
        self.modifier = ValueModifier(self.db_path, refresh_interval=5, preload=False)

    @patch("functions.value_modifier.sqlite3.connect")
    @patch("functions.value_modifier.time.time")
    def test_refresh_called_on_get_multiplier(self, mock_time, mock_connect):
        mock_time.return_value = 1000

        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            ("INSTRUMENT_A", 1.5),
            ("INSTRUMENT_B", 2.0)
        ]

        self.modifier._refresh()

        multiplier = self.modifier.get_multiplier("INSTRUMENT_A")

        mock_connect.assert_called_once_with(self.db_path)
        mock_cursor.execute.assert_called_once_with("SELECT NAME, MULTIPLIER FROM INSTRUMENT_PRICE_MODIFIER")

        self.assertEqual(multiplier, 1.5)
        self.assertEqual(self.modifier.last_refresh, 1000)
        self.assertDictEqual(self.modifier._modifiers, {
            "INSTRUMENT_A": 1.5,
            "INSTRUMENT_B": 2.0
        })

    @patch("functions.value_modifier.sqlite3.connect")
    @patch("functions.value_modifier.time.time")
    def test_get_multiplier_returns_1_for_unknown(self, mock_time, mock_connect):
        self.modifier._modifiers = {"INSTRUMENT_A": 1.5}
        self.modifier.last_refresh = 1000
        mock_time.return_value = 1002

        multiplier = self.modifier.get_multiplier("UNKNOWN")

        mock_connect.assert_not_called()
        self.assertEqual(multiplier, 1.0)

    @patch("functions.value_modifier.time.time")
    @patch("functions.value_modifier.sqlite3.connect")
    def test_refresh_called_only_after_interval(self, mock_connect, mock_time):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = [("X", 3.0)]

        mock_time.return_value = 1000
        self.modifier._refresh()

        mock_time.return_value = 1003
        self.modifier.get_multiplier("X")
        mock_connect.assert_called_once()

        mock_time.return_value = 1006
        self.modifier.get_multiplier("X")
        self.assertEqual(mock_connect.call_count, 2)

    @patch("functions.value_modifier.logging.getLogger")
    @patch("functions.value_modifier.sqlite3.connect")
    def test_refresh_handles_exception_and_logs_error(self, mock_connect, mock_get_logger):
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger
        modifier = ValueModifier(self.db_path, preload=False)
        mock_connect.side_effect = Exception("DB connection error")

        modifier._refresh()

        mock_logger.error.assert_called_once()
        args, _ = mock_logger.error.call_args
        assert "Failed to refresh modifiers" in args[0]
        assert "DB connection error" in args[0]

if __name__ == "__main__":
    unittest.main()