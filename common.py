import os, glob, shutil
import xml.etree.ElementTree as ET
from datetime import datetime
from const import intersection_data_location


def get_csv_paths(intersection_name) -> list:
    return glob.glob(os.path.join(intersection_data_location, intersection_name, '*.csv'))


def get_xml_path(intersection_name):
    return glob.glob(os.path.join(intersection_data_location, intersection_name, '*.xml'))[0]


def to_datetime(time):
    return datetime.strptime(time, '%d-%m-%Y %H:%M:%S.%f')


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


def datetime_string_to_milli(datetime_string) -> int:
    """Datetime in string format '%d-%m-%Y %H:%M:%S.%f' to milliseconds since 1970"""
    return int(datetime.strptime(datetime_string, '%d-%m-%Y %H:%M:%S.%f').timestamp()*1000)


def open_xml(file_name):
    """
    Returns a xml out of the given directory.
    
    :param file_name: the name of the xml put in like this -> 'BOS210/79190154_BOS210_ITF_COMPLETE.xml'
    :type str

    :returns: an xml readable in python
    :type xml.Element
    """
    path = os.getcwd()
    # if not(path.endswith("VIS-group-C")):
    #     os.chdir("..")
    file = get_xml_path(file_name)
    
    tree = ET.parse(file)
    root = tree.getroot()
    return root


def move_file(file_name, map_name_out, map_name_in):
    """
    Moves a single file from map_name_in to map_name_out
    """
    source = os.path.join('', map_name_out, file_name)
    target = os.path.join('', map_name_in)
    file_check = os.path.join(target, file_name)
    if os.path.exists(file_check):
        os.remove(file_check)
    shutil.move(source,target)


def create_csv_file(data, path_with_filename):
    """
    Create a csv file containing the giving data at the place of path_with_filename. Which contains
    that will be given to the file.
    """
    if os.path.exists(path_with_filename):
        os.remove(path_with_filename)
    data.to_csv(path_with_filename, index=False, sep=';')


def clear_cars_movements():
    """Clears the cars_movemenets folder from all csv's"""
    all_files = glob.glob(os.path.join("cars_movements", '*.csv'))
    for file in all_files:
        try:
            if file.endswith(glob.glob(os.path.join("cars_movements","ext_*.csv"))[0]):
                continue
        except:
            os.remove(file)
