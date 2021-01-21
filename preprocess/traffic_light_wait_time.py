import xml.etree.ElementTree as ET
import sys
import numpy as np
import os
import glob
import pandas as pd

sys.path.append('./')
from common import *
from preprocess.lane_technical_information import get_dict_lane_info

def extract_info_csv(intersection, dict_avg_time_per_lane):
    df = pd.read_csv('./intersections/{}/compressed/compressed.csv'.format(intersection), delimiter=';')
    dict_with_lane_info = get_dict_lane_info(intersection)
    
    for lane_id in dict_with_lane_info.keys():
        sensor_closest_by_intersection = dict_with_lane_info[lane_id]['induction_loops'][0]
        df.set_index('start_time')
        df_select_columns = df[['start_time', 'end_time', sensor_closest_by_intersection]]
        
        for _, row in df_select_columns.iterrows():
            if row[sensor_closest_by_intersection] == '|':
                time = (row['end_time'] - row['start_time']) / 1000
                if time > 1.0:
                    if lane_id in dict_avg_time_per_lane:
                        dict_avg_time_per_lane[lane_id].append(time)
                    else:
                        dict_avg_time_per_lane[lane_id] = [time]
    
    return dict_avg_time_per_lane

def calculate_avg_waitingtime():
    """Calculates avg time of trafficlight waiting time"""

    dict_avg_time_per_lane = {}
    intersection_list = os.listdir('./intersections')
    for intersection in intersection_list:
        if intersection == ".keep":
            continue
        dict_avg_time_per_lane = extract_info_csv(intersection, dict_avg_time_per_lane)
    dict_avg_time_per_lane_calculated = {}
    for key in dict_avg_time_per_lane:
        dict_avg_time_per_lane_calculated[key] = np.mean(dict_avg_time_per_lane[key])
                    
    return dict_avg_time_per_lane_calculated   

if __name__ == "__main__":
    print(calculate_avg_waitingtime())