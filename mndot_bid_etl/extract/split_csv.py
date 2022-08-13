import re


def split_csv(csv_file) -> list[str]:
    """Splits the csv data by blank lines to divide into its three subtables"""
    blank_line_regex = r"(?:\r?\n){2,}"
    with open(csv_file, "r") as f:
        return re.split(blank_line_regex, f.read())
