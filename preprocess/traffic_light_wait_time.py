import xml.etree.ElementTree as ET
import sys
import numpy as np
import os
import glob
import pandas as pd
from processing_module import get_car_spawn_times

sys.path.append('./')

from common import open_xml
from lane_technical_information import get_dict_lane_info

def extract_info_csv(csv_files, csv_file):
    df = pd.read_csv("./intersections/{}/{}".format(csv_files, csv_file))
    
    dict_with_lane_info = get_dict_lane_info(csv_files)
    
    for lane_id in dict_with_lane_info.keys():
        sensor_closest_by_intersection = dict_with_lane_info[lane_id]['induction_loops'][0]
        traffic_light = dict_with_lane_info[lane_id]['traffic_light']
        induction_loop_time_high = get_car_spawn_times(df, sensor_closest_by_intersection)
        df.set_index('time')
        for time_unit in induction_loop_time_high:
            specific_sensor_and_trafficlight = df[traffic_light, sensor_closest_by_intersection] # drop all collumn behalve de huidige stoplicht en dichtstbijzijnde sensor.
            # TODO Check voor iedere keer dat in het csv bestand de sensor_closest_by_intersection en traffic_light aan staan en rood (en oranje?) zijn. Tel deze tijd bij elkaar op.
            # TODO geef het gemiddelde wachttijd terug per lane.

def calculate_avg_waitingtime(file_name):
    """Calculates avg time of trafficlight waiting time"""
    
    #xml_file = open_xml(file_name)
    
    avg_time = []

    for csv_files in os.listdir('./intersections'):
        path = os.path.join('intersections', csv_files)
        if os.path.isdir(path):
            for csv_file in os.listdir(path):
                if csv_file.endswith('.csv'):
                    avg_waitingtime_per_intersection = extract_info_csv(csv_files, csv_file)
                    
                    
    return np.mean(avg_time)    

if __name__ == "__main__":
    file_name = "BOS210"
    calculate_avg_waitingtime(file_name)