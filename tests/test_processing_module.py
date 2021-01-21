from unittest import TestCase
import xml.etree.ElementTree as ET
import pandas as pd
import os

from preprocess.processing_module import get_coordinates_lane, get_all_lanes_coordinates, \
    get_geoposities, extract_lane_id, get_car_spawn_times, vehicles_laneID, calculate_trajectory, get_nodes, get_lane, get_coordinates
from common import open_xml

class Test(TestCase):

    def test_get_car_spawn_times(self):
        test_csv_path = os.path.join("tests","filetest", "testcsvfile.csv")
        list_columns = ["03", "k103"]
        expected_output = {"03": ["02-11-2020 00:00:00.9", "02-11-2020 00:00:07.9"],
                           "k103": ["02-11-2020 00:00:00.3", "02-11-2020 00:00:04.2"]}

        spawn_times = get_car_spawn_times(test_csv_path, list_columns)

        self.assertEqual(spawn_times, expected_output)
    
    def test_calculate_trajectory(self):
        actual_distance = 0.038245325870749115 #  the trajectory of igresslane 2 and egresslane 19
        # get the start and en dcoordinates of the trajectory 
        start_coordinate = [51.6831293, 5.2938658]
        end_coordinate = [51.6829984, 5.2943788]
        
        test_distance = calculate_trajectory(start_coordinate[1], start_coordinate[0], end_coordinate[1],end_coordinate[0])
        self.assertEqual(test_distance, actual_distance)

    def test_vehicles_laneID(self):
        root = open_xml('BOS210')
        actual_lanes = ['1', '2', '7', '8', '12', '13', '14', '15', '17', '18', '19', '20', '26']
        test_lanes = list(vehicles_laneID(root).keys() )# returns dict_keys, convert to list 
        
        self.assertEqual(test_lanes, actual_lanes)

    def test_get_nodes(self):
        root = open_xml('BOS210')
        # get the coordinates of lane 14 from xml file
        coordinates14 = [[51.682829, 5.2942043], [51.6827282, 5.2942427], [51.6826642, 5.2942515], [51.6825888, 5.2942495], [51.6825214, 5.294241], [51.6817411, 5.2940632], [51.6815636, 5.2940316], [51.681504, 5.2940671]]
        print("Actual")
        print(coordinates14)
        nodes14 = root[2][1][0][6][13][4] # nodes Element of lane 14 halen from xml file
        test_coord = get_nodes(nodes14)
        print('Expected')
        print(test_coord)
        self.assertEqual(test_coord, coordinates14)

    def test_get_lane(self):
        root = open_xml('BOS210')
        actual_genericlane = root[2][1][0][6][0] # getting the first genericlane
        test_genericlane = get_lane(root, "1") 
        self.assertEqual(test_genericlane, actual_genericlane)
    
    def test_get_coordinates_trajectory(self):
        actual_coordinates_1 = [[51.683119, 5.2938207], [51.6830587, 5.2938612], [51.6829923, 5.293916], [51.6829464, 5.2939591], [51.6828937, 5.2940163], [51.6828124, 5.2941116]]
        root = open_xml('BOS210')
        lane1 = root[2][1][0][6][0] # getting the first genericlane
        test_coord = get_coordinates(root, lane1, 'trajectory')
        self.assertEqual(test_coord, actual_coordinates_1)

        
        


