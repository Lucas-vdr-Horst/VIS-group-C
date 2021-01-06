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

    coordinaten = []
    for i in root[2][1][0][6]: # for item in 
        for node in i.iter('nodes'): # for lane in Laneset
            for n in node[0].iter('node-LatLon'):
                lon = int(n.findall('lon')[0].text)
                lat = int(n.findall('lat')[0].text)
                coordinaten.append([lon, lat])
                print(lon, lat)
    print(coordinaten)
if __name__ == "__main__":
    process("02-11-2020 00:00:00.0","02-11-2020 00:00:00.6")



# [     long       lat         long     lat       long      lat
#   [[378328794, 4893289004], [893924, 483724], [48328094, 38492043]],  auto1
#   [[378328794, 4893289004], [893924, 483724], [48328094, 38492043]],  auto2
#   [[378328794, 4893289004], [893924, 483724], [48328094, 38492043]]   auto3
# ]

