from const import intersection_data_location
import os
import csv
import math
from common import get_available_intersections
import pandas as pd

class SignalManager:


    def __init__(self, csv_path: [str]):
        self.csv_path = csv_path 
        #Read csv's
        #self.reader = self.make_reader()
        self.reader= {
            'BOS210': csv_path[0],
            'BOS211': csv_path[1]
        }
    
        # self.reader = {
        #     'BOS210': csv.reader(csv_path[0]),
        #     'BOS211': csv.reader(csv_path[1])
        # }
        # TODO: Make readers variable
        # for path in csv_path
        #     self.reader[path] = csv.reader(path)
        


    def getState(self, columnName, time, intersectionPlace):
        #path = os.path.join(intersection_data_location, intersectionPlace, "compressed", "compressed.csv")
        path = self.reader[intersectionPlace]
        df = pd.read_csv(path,delimiter=";", dtype=str)
        # df.set_index('start_time')
        # x = df.iloc[(df[time]>= df.start_time) & (df[time]>= df.end_time)][columnName]
        df[['start_time', 'end_time']] = df[['start_time', 'end_time']].astype('int64')#.apply(lambda x: float(x))
        return df[columnName][(df['start_time'] >= time) and (df['end_time'] <= time)]
    
    def test(self, intersection):
        inputs_blocks = []
        filepath = os.path.join(intersection_data_location, intersection, 'compressed', 'compressed.csv')
        lengenda = tuple(filter(lambda l: len(l.split(';')) > 1, open(filepath).read().split('\n')[0])) # TODO misschien niet nodig #TODO klopt niet.
        lines = tuple(filter(lambda l: len(l.split(';')) > 1, open(filepath).read().split('\n')[1:]))
        for line in lines:
            split = line.split(';')
            inputs_blocks.append({
                int(split[0]) : split[2:] #{1478935 : [,,,,,,,,,#,,,#,,,,,}
            })
        return inputs_blocks
    
    def make_reader(self):
        reader = {}
        for intersection in get_available_intersections():
            with open(os.path.join(intersection_data_location, intersection, "compressed", "compressed.csv")) as csvfile:
                print(csvfile)
                reader[intersection] = csv.reader(csvfile, delimiter=';')
                # for row in reader.get(intersection)[:10]:
                #     print(row)
                # print(reader[intersection])
        return reader
