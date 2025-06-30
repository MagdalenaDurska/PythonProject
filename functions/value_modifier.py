import sqlite3
import time
import logging

class ValueModifier:
    def __init__(self, db_path, refresh_interval=5, preload=True, logger=None):
        self.db_path = db_path
        self.refresh_interval = refresh_interval
        self._modifiers = {}
        self.last_refresh = 0
        self.logger = logger or logging.getLogger(__name__)
        if preload:
            self._refresh()

    def _refresh(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT NAME, MULTIPLIER FROM INSTRUMENT_PRICE_MODIFIER")
                rows = cursor.fetchall()
                self._modifiers = {
                    name: float(multiplier)
                    for name, multiplier in rows
                    if name and multiplier is not None
                }
                self.last_refresh = time.time()
        except Exception as e:
            self.logger.error(f"Failed to refresh modifiers: {e}")

    def get_multiplier(self, instrument):
        now = time.time()
        elapsed = now - self.last_refresh

        if elapsed > self.refresh_interval:
            self._refresh()

        return self._modifiers.get(instrument, 1.0)