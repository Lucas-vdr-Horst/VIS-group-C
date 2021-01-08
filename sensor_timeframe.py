import datetime
import json
import os
import glob
from common import read_intersection_csvs, to_datetime
import pandas as pd
import numpy as np
from alive_progress import alive_bar

intersection_data_location = os.path.join('intersections', '')


def to_ms_since_1970(datetime_frame):
    """
    converts datetime to milisec
    Bron: https://stackoverflow.com/questions/6999726/how-can-i-convert-a-datetime-object-to-milliseconds-since-epoch-unix-time-in-p
    """
    datetime_frame = to_datetime(datetime_frame)
    utc_timestamp = datetime.datetime.utcfromtimestamp(0)
    return int((datetime_frame - utc_timestamp).total_seconds() * 1000.0)


def remove_json_file_if_exist(file):
    sensor_file = os.path.join('preprocessed', 'sensor_preproces.json')  # path to json file
    if os.path.exists(sensor_file):  # deletes json file to prevent duplicate if exist
        os.remove(sensor_file)


def read_and_transepose_csv(csv):
    df = pd.read_csv(csv, sep=';', low_memory=False)
    df = df.replace(np.nan, '', regex=True)
    df['time'] = df['time'].apply(to_ms_since_1970)
    df2 = df.set_index('time')
    df2 = df2.transpose()
    temp_dict = df2.to_dict()
    return df, temp_dict


def sensor_timeframe():
    # TODO
    sensor_file = os.path.join('preprocessed','sensor_preproces.json')  # path to json file
    remove_json_file_if_exist(sensor_file)
    sensor_dict = {}
    all_intersection_names = [i[14:] for i in glob.glob(os.path.join(intersection_data_location, '*'))]
    for intersection_name in all_intersection_names:
        csvs = read_intersection_csvs(intersection_name)
        for csv in csvs:
            df, temp_dict = read_and_transepose_csv(csv)
            with alive_bar(len(df)) as bar:
                for time_frame in df['time']:
                    if time_frame in sensor_dict:
                        sensor_dict[time_frame].update({intersection_name : temp_dict[time_frame]})
                    else:
                        sensor_dict[time_frame] = {intersection_name : temp_dict[time_frame]}
                    bar()
    with open(sensor_file, "w") as f:   # upload dictonary with data to json file
        json.dump(sensor_dict, f, indent=2)


if __name__ == "__main__":
    sensor_timeframe()
