import time
import os
from datetime import datetime
from functions.config import FILTERS, INSTRUMENTS


def is_selected_date(date):
    return date.year == FILTERS["YEAR"] and date.month == FILTERS["MONTH"]


def format_results(results):
    return (
        "=== Computation Results ===\n"
        f"Mean for instrument {INSTRUMENTS['MEAN']}: {results['mean']:.2f}\n"
        f"Mean for instrument {INSTRUMENTS['MEAN_DATE']} for date {FILTERS['MONTH']}/{FILTERS['YEAR']}: {results['mean_selected_date']:.2f}\n"
        f"Sum of latest 10 values for instruments other than {INSTRUMENTS['MEAN']}, {INSTRUMENTS['MEAN_DATE']} and {INSTRUMENTS['STDDEV']}: {results['latest_sum']:.2f}\n"
        f"Standard deviation for instrument {INSTRUMENTS['STDDEV']}: {results['stddev']:.2f}\n"
    )

def save_results(formatted_results, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    time_now = time.time()
    out_path = os.path.join(output_dir, f"results_{time_now:.0f}.txt").replace('\\', '/')
    with open(out_path, "w") as f:
        f.write(formatted_results)
    print(f"Results saved to {out_path}")

def handle_output(results, output_dir):
    formatted = format_results(results)
    print(formatted)
    save_results(formatted, output_dir)