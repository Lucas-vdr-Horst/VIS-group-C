from unittest import TestCase
from processing_module import calculate_markers_points, get_coordinates_lane, get_all_lanes_coordinates, process
import xml.etree.ElementTree as ET
import pandas as pd



class Test(TestCase):
    def test_calculate_markers_points(self):
        lane13 = [51.6828358, 5.2942547]
        lane19 = [51.6829984, 5.2943788]
        print(type(lane19[0]))
        calulated_path = calculate_markers_points(lat1=lane13[0], lon1=lane13[1], lat2=lane19[0], lon2=lane19[1], marker_count=5)
        self.assertEqual(len(calulated_path), 5)
    
    def test_get_coordinates_lane_ingress(self):
        lane14 = [[51.681504, 5.2940671], [51.6815636, 5.2940316], [51.6817411, 5.2940632], [51.6825214, 5.294241], 
        [51.6825888, 5.2942495], [51.6826642, 5.2942515], [51.6827282, 5.2942427], [51.682829, 5.2942043], [51.682829, 5.2942043], 
        [51.682872, 5.2941821], [51.6829149, 5.2941497], [51.6830158, 5.2940584], [51.6830734, 5.2940079], [51.6831515, 5.2939548]]

        tree = ET.parse('intersections/BOS210/79190154_BOS210_ITF_COMPLETE.xml') # parse given XML file
        root = tree.getroot()
        genericlane14 = root[2][1][0][6][13] # get genericlane of lane 14
        coord14 = get_coordinates_lane(genericlane14)

        self.assertEqual(coord14, lane14)
    
    def test_get_coordinates_lane_engress(self):
        lane15 = [[51.6831515, 5.2939548], [51.6831954, 5.2939272], [51.6832501, 5.293898], [51.6833342, 5.2938686], 
        [51.6834031, 5.2938528], [51.6834978, 5.293851], [51.683597, 5.2938652], [51.6836913, 5.2938935], [51.6837799, 5.2939392], 
        [51.6838241, 5.2939473], [51.6838723, 5.2939387], [51.6839068, 5.2939185], [51.6839596, 5.2938718], [51.6840238, 5.2937591], [51.6842327, 5.2933148]]  

        tree = ET.parse('intersections/BOS210/79190154_BOS210_ITF_COMPLETE.xml') # parse given XML file
        root = tree.getroot()
        genericlane15 = root[2][1][0][6][14] # get genericlane of lane 14
        coord15 = get_coordinates_lane(genericlane15)

        self.assertEqual(coord15, lane15)
    
    def test_get_all_lanes_coordinates(self):
        #TODO test df and paden_test
        df = pd.read_csv('paden_autos')
        print(df)
        tree = ET.parse('intersections/BOS210/79190154_BOS210_ITF_COMPLETE.xml') # parse given XML file
        paden_test = get_all_lanes_coordinates(tree)
        
        for i in range(df['coordinaten'].shape[0]):
            print(df.loc[i,'Rijbaan'])
            self.assertEqual(df.loc[i, 'coordinaten'],paden_test.loc[i, 'coordinaten'] )
        
        


