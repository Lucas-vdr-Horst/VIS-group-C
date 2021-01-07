import os
import glob
from datetime import datetime


def read_csvs(intersection_name):
    intersection_data_location = os.path.join('intersections', '')
    return glob.glob(os.path.join(intersection_data_location, intersection_name, '*.csv'))

def to_datetime(time):
    return datetime.strptime(time, '%d-%m-%Y %H:%M:%S.%f')