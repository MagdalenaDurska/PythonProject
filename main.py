import argparse
import os
from functions.processor import FileProcessor
from functions.utils import handle_output


def main():
    parser = argparse.ArgumentParser(description="Process instrument data file.")

    parser.add_argument(
        "--input", "-i",
        help="Path to input data file"
    )
    parser.add_argument(
        "--output-dir", "-o",
        help="Directory to save results"
    )
    parser.add_argument(
        "--batch", "-b",
        action="store_true",
        help="Run in batch mode using default file locations"
    )

    args = parser.parse_args()

    if args.batch:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        input_path = os.path.join(base_dir, "input/input.txt")
        output_dir = os.path.join(base_dir, "output")
    else:
        if not args.input or not args.output_dir:
            parser.error("--input and --output-dir are required unless --batch is specified")
        input_path = args.input
        output_dir = args.output_dir

    log_file_path = os.path.join(output_dir, "logs.txt")

    processor = FileProcessor(input_path, log_file_path)
    processor.process()
    results = processor.results()

    handle_output(results, output_dir)


if __name__ == "__main__":
    main()
