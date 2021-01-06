import pandas as pd
from pathlib import Path
from data_cleaning import fix_hashtags
import xml.etree.ElementTree as ET


def process(begin_time, end_time):
    """
    Geeft json terug iets zoals hier beneden

    :param begin_time: als 554. Dit betekend 00 uur 00 min 55 sec .4 milisec
    :type str

    :param end_time: als 554. Dit betekend 00 uur 00 min 55 sec .4 milisec
    :type str"""

    # if not Path("./dataset/sensor_data/new_BOS210.csv").is_file():
    #     fix_hashtags("BOS210.csv")
    # df_sensor = pd.read_csv("./dataset/sensor_data/new_BOS210.csv", delimiter=";", low_memory=False)
    # df_sensor = df_sensor.set_index('time') # set index to time
    # data = df_sensor.loc[begin_time:end_time] # filter to begin and end time

    tree = ET.parse('./dataset/layouts/79190154_BOS210_ITF_COMPLETE.xml')
    root = tree.getroot()

    dict_with_coords = {}
    for genericlane in root[2][1][0][6]: # i == generic lane
        laneId = int(genericlane.find('laneID').text) # haal uit laneId
        coordinaten = [] 
        # Haal alle longitude en latitude uit nodes-La
        for node in genericlane.iter('nodes'): # i.iter('nodes') == nodes

            for n in node.iter('node-LatLon'): # node.iter('node-LatLon') == node-latlon
                lon = int(n.findall('lon')[0].text)
                lat = int(n.findall('lat')[0].text)
                coordinaten.append([lon, lat])
        dict_with_coords[laneId] = coordinaten
    return dict_with_coords
    
if __name__ == "__main__":
    process("02-11-2020 00:00:00.0","02-11-2020 00:00:00.6")



# [     long       lat         long     lat       long      lat
#   [[378328794, 4893289004], [893924, 483724], [48328094, 38492043]],  auto1
#   [[378328794, 4893289004], [893924, 483724], [48328094, 38492043]],  auto2
#   [[378328794, 4893289004], [893924, 483724], [48328094, 38492043]]   auto3
# ]

