import os
import glob
from datetime import datetime


def read_csvs(intersection_name):
    intersection_data_location = os.path.join('intersections', '')
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
        datetime.strptime(read_lines(filename, [1])[1].split(';')[0], '%d-%m-%Y %H:%M:%S.%f'),
        len(open(filename).readlines())-1
    )
