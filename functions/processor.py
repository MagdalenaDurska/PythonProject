from functions.models import DataRow
from functions.calculators import (
    MeanCalculator,
    LatestSumCalculator,
    MeanStdDevCalculator
)
from functions.utils import is_selected_date
from functions.logger import setup_logger
from functions.config import (
    INSTRUMENTS,
    TOP_N,
    VALUE_MODIFIER_DB_PATH
)
from functions.value_modifier import ValueModifier

class FileProcessor:
    def __init__(self, filepath, log_file, db_path=VALUE_MODIFIER_DB_PATH):
        self.filepath = filepath
        self.value_modifier = ValueModifier(db_path)
        self.mean = MeanCalculator(INSTRUMENTS["MEAN"])
        self.mean_selected_date = MeanCalculator(INSTRUMENTS["MEAN_DATE"], date_filter=is_selected_date)
        self.latest_sum_calc = LatestSumCalculator(exclude_instruments=[INSTRUMENTS["MEAN"], INSTRUMENTS["MEAN_DATE"], INSTRUMENTS["STDDEV"]], top_n=TOP_N)
        self.stddev= MeanStdDevCalculator(INSTRUMENTS["STDDEV"])
        self.logger = setup_logger(log_file)
        self.processed_rows = 0

    def process_line(self, line, line_number):
        try:
            row = DataRow.from_csv_line(line)

            multiplier = self.value_modifier.get_multiplier(row.instrument)
            row.value *= multiplier

            self.logger.debug(f"Processing line {line_number}")
            self.mean.process(row)
            self.mean_selected_date.process(row)
            self.latest_sum_calc.process(row)
            self.stddev.process(row)

            self.processed_rows += 1

        except ValueError as ve:
            self.logger.warning(f"Line {line_number}: Parsing error - {ve}")
        except Exception as e:
            self.logger.exception(f"Line {line_number}: Unexpected error")


    def process(self) :
        self.logger.info(f"Started processing: {self.filepath}")
        try:
            with open(self.filepath, 'r') as f:
                for line_number, line in enumerate(f, 1):
                    self.process_line(line, line_number)

        except FileNotFoundError:
            self.logger.error(f"File not found: {self.filepath}")
        except Exception as e:
            self.logger.exception(f"Unexpected error while processing file: {e}")
        finally:
            self.logger.info("Finished processing")
            self.logger.info(f"Number of processed rows: {self.processed_rows}")


    def results(self):
        return {
            "mean": self.mean.mean_result(),
            "mean_selected_date": self.mean_selected_date.mean_result(),
            "latest_sum": self.latest_sum_calc.sum_result(),
            "stddev": self.stddev.stddev_result()
        }