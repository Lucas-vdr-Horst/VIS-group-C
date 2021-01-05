import pandas as pd
from pathlib import Path
from data_cleaning import fix_hashtags

def process(begin_time, end_time):
    """
    Geeft json terug iets zoals hier beneden

    :param begin_time: als 554. Dit betekend 00 uur 00 min 55 sec .4 milisec
    :type str

    :param end_time: als 554. Dit betekend 00 uur 00 min 55 sec .4 milisec
    :type str"""

    if not Path("./dataset/sensor_data/new_BOS210.csv").is_file():
        fix_hashtags("BOS210.csv")
    df_sensor = pd.read_csv("./dataset/sensor_data/new_BOS210.csv", delimiter=";", low_memory=False)
    data = df_sensor.iloc[begin_time:end_time]

if __name__ == "__main__":
    process(554, 556)

# [     long       lat         long     lat       long      lat
#   [[378328794, 4893289004], [893924, 483724], [48328094, 38492043]],  auto1
#   [[378328794, 4893289004], [893924, 483724], [48328094, 38492043]],  auto2
#   [[378328794, 4893289004], [893924, 483724], [48328094, 38492043]]   auto3
# ]                    
