import os
import glob
from datetime import datetime
from const import intersection_data_location


def get_csv_paths(intersection_name) -> list:
    return glob.glob(os.path.join(intersection_data_location, intersection_name, '*.csv'))


def read_lines(filename: str, lines: list) -> dict:
    """Reads specific lines of a file"""
    result = {}
    last = max(lines)
    for i, line in enumerate(open(filename)):
        if i in lines:
            result[i] = line[:-1]
        elif i > last:
            break
    return result


def timeframe_csv(filename: str):
    return (
        read_lines(filename, [1])[1].split(';')[0],
        len(open(filename).readlines())-1
    )


def get_available_intersections() -> list:
    return [i.replace(intersection_data_location, '') for i in glob.glob(os.path.join(intersection_data_location, '*'))]


def get_header(csv_filepath: str) -> str:
    return read_lines(csv_filepath, [0])[0]
