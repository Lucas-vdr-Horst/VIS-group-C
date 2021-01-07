import pandas as pd
from pathlib import Path
from data_cleaning import fix_hashtags
import xml.etree.ElementTree as ET
import json
import os


intersection_data_location = os.path.join('intersections', '')


def load_sensor_data(begin_time, end_time, intersection_name):
    if not Path(os.path.join(intersection_data_location, intersection_name, '*.csv')).is_file():  #TODO verwijder deze en volgende regel wanneer schone data is aangeleverd door Vialis
         fix_hashtags("BOS210.csv")
    df_sensor = pd.read_csv(os.path.join(intersection_data_location, intersection_name, '*.csv'), delimiter=";", low_memory=False)
    df_sensor = df_sensor.set_index('time') # set index to time
    data_sensor_specific_time = df_sensor.loc[begin_time:end_time] # filter to begin and end time
    return data_sensor_specific_time


def get_coordinates_lane(genericlane):
    """Haal alle longitude en latitude uit nodes van gegeven laneID"""
    coordinaten = [] 
    for node in genericlane.iter('nodes'): # i.iter('nodes') == nodes
            for n in node.iter('node-LatLon'): # node.iter('node-LatLon') == node-latlon
                lon = int(n.findall('lon')[0].text)
                lat = int(n.findall('lat')[0].text)
                coordinaten.append([lon, lat])
    return coordinaten


def json_file_all_lanes_coordinates(tree):
    root = tree.getroot()
    dict_with_coords = {}
    for genericlane in root[2][1][0][6]: # i == generic lane
        # Pak je de laneID van genericlane en de connected lane
        if genericlane[3][2].tag == 'vehicle': # pak de lanes voor auto's 
            laneId = int(genericlane.find('laneID').text) # haal uit laneId
            # Pak de coordinaten van genericlane
            coordinaten_lane_in = get_coordinates_lane(genericlane)
            # Pak de lane id van de lane die gekoppeld is aan laneId - gekoppelde egresslane
            if genericlane.find('connectsTo'):
                for i in genericlane.iter('connectsTo'):
                    connected_to = i[0][0][0].text

        for lane in root[2][1][0][6]:
            if lane[0].text == connected_to:
                connected_to_lane = lane
        
        # Haal uit de coordinaten van de gekoppelde egresslane uit de dictionary  en voeg het toe in dict_with_coords[laneId]
        coordinaten_lane_out = get_coordinates_lane(connected_to_lane)
        dict_with_coords[laneId] = coordinaten_lane_in + coordinaten_lane_out
    # TODO de trajectory berekenen van een lane 
    json_file = json.dumps(dict_with_coords)
    return json_file


def process(begin_time, end_time):
    """
    Geeft json terug iets zoals hier beneden

    :param begin_time: als 554. Dit betekend 00 uur 00 min 55 sec .4 milisec
    :type str

    :param end_time: als 554. Dit betekend 00 uur 00 min 55 sec .4 milisec
    :type str"""

    sensor_data = load_sensor_data(begin_time, end_time, "BOS210")

    tree = ET.parse(os.path.join(intersection_data_location, "BOS210", '*.csv'))
    json_file = json_file_all_lanes_coordinates(tree)

    # TODO: voor iedere rij in sensordata check of sensor geraakt wordt. wanneer een sensor geraakt wordt zoek welke lane deze sensor zit en voeg de coordinaten voor die lane toe aan returnvalue

    # return een file met alle auto's die rijden op dat moment
    
    return json_file


if __name__ == "__main__":
    process("02-11-2020 00:00:00.0", "02-11-2020 00:00:00.6")


# [     long       lat         long     lat       long      lat
#   [[378328794, 4893289004], [893924, 483724], [48328094, 38492043]],  auto1
#   [[378328794, 4893289004], [893924, 483724], [48328094, 38492043]],  auto2
#   [[378328794, 4893289004], [893924, 483724], [48328094, 38492043]]   auto3
# ]

