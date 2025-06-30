import argparse
import os
from functions.processor import FileProcessor
from functions.utils import handle_output

def main():
    parser = argparse.ArgumentParser(description="Process instrument data file.")
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to input data file"
    )
    parser.add_argument(
        "--output-dir", "-o",
        required=True,
        help=f"Directory to save results"
    )
    parser.add_argument(
        "--log-file", "-l",
        required=False,
        default=None,
        help="Path to log file (default: output_dir/logs.txt)"
    )
    args = parser.parse_args()

    if args.log_file is None:
        args.log_file = os.path.join(args.output_dir, "logs.txt")

    processor = FileProcessor(args.input, args.log_file)
    processor.process()
    results = processor.results()

    handle_output(results, args.output_dir)


if __name__ == "__main__":
    main()
