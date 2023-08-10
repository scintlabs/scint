import os
import sys
import logging


def tasks(directory, output_file, search_strings, file_types, ignore_case=False):
    string_counts = {string: 0 for string in search_strings}
    logging.basicConfig(filename="scan_log.log", level=logging.INFO)

    try:
        with open(output_file, "w") as report:
            for foldername, subfolders, filenames in os.walk(directory):
                for filename in filenames:
                    if filename.endswith(tuple(file_types)):
                        file_path = os.path.join(foldername, filename)
                        with open(file_path, "r", encoding="utf-8") as file:
                            for line_no, line in enumerate(file):
                                for string in search_strings:
                                    if (
                                        ignore_case and string.lower() in line.lower()
                                    ) or (not ignore_case and string in line):
                                        string_counts[string] += 1
                                        report.write(
                                            f"{file_path}:{line_no}:{string}:{line.strip()}\n"
                                        )
        report.write("\nSummary:\n")
        for string, count in string_counts.items():
            report.write(f"{string}: found {count} times\n")
    except Exception as e:
        logging.error("An error occurred:", exc_info=True)


if __name__ == "__tasks__":
    try:
        directory = sys.argv[1]
        output_file = sys.argv[2]
        search_strings = sys.argv[3].split(",")
        file_types = tuple(sys.argv[4].split(","))
        ignore_case = sys.argv[5].lower() == "true"
        tasks(directory, output_file, search_strings, file_types, ignore_case)
        print(f"Report generated: {output_file}")
    except IndexError:
        print("Please specify all command-line arguments.")
    except Exception as e:
        print(f"An error occurred: {e}")
