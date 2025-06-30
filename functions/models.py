from dataclasses import dataclass
from datetime import datetime

@dataclass
class DataRow:
    instrument: str
    date: datetime
    value: float

    @classmethod
    def from_csv_line(cls, line):
        try:
            parts = line.strip().split(',')
            if len(parts) != 3:
                raise ValueError("Line does not have exactly 3 columns")

            if any(not p for p in parts):
                raise ValueError("One or more fields are empty")

            instrument = parts[0].strip()
            date = datetime.strptime(parts[1].strip(), "%d-%b-%Y")
            value = float(parts[2].strip())
            return cls(instrument, date, value)

        except ValueError as ve:
            raise ValueError(f"Error parsing line '{line.strip()}': {ve}")