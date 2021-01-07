import os
import glob


def read_csvs(intersection_name):
    intersection_data_location = os.path.join('intersections', '')
    return glob.glob(os.path.join(intersection_data_location, intersection_name, '*.csv'))