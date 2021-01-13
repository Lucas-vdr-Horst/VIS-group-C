from unittest import TestCase
from processing_module import calculate_markers_points, get_coordinates_lane, get_all_lanes_coordinates, process, get_geoposities, extract_lane_id
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
        tree = ET.parse('intersections/BOS210/79190154_BOS210_ITF_COMPLETE.xml')
        root = tree.getroot()
        genericlane14 = root[2][1][0][6][13] # get genericlane of lane 14
        coord14 = get_coordinates_lane(genericlane14)

        self.assertEqual(coord14, lane14)
    
    def test_get_coordinates_lane_engress(self):
        lane15 = [[51.6831515, 5.2939548], [51.6831954, 5.2939272], [51.6832501, 5.293898], [51.6833342, 5.2938686], 
        [51.6834031, 5.2938528], [51.6834978, 5.293851], [51.683597, 5.2938652], [51.6836913, 5.2938935], [51.6837799, 5.2939392], 
        [51.6838241, 5.2939473], [51.6838723, 5.2939387], [51.6839068, 5.2939185], [51.6839596, 5.2938718], [51.6840238, 5.2937591], [51.6842327, 5.2933148]]  
        tree = ET.parse('intersections/BOS210/79190154_BOS210_ITF_COMPLETE.xml')
        root = tree.getroot()
        genericlane15 = root[2][1][0][6][14] # get genericlane of lane 14
        coord15 = get_coordinates_lane(genericlane15)

        self.assertEqual(coord15, lane15)
    
    #TODO verbeter test_get_all_lanes_coordinates
    def test_get_all_lanes_coordinates(self):
        #TODO test df and paden_test
        df = pd.read_csv('paden_autos')
        tree = ET.parse('intersections/BOS210/79190154_BOS210_ITF_COMPLETE.xml')
        print(df) # parse given XML file
        paden_test = get_all_lanes_coordinates(tree)
        
        for i in range(df['coordinaten'].shape[0]):
            print(df.loc[i,'Rijbaan'])
            self.assertEqual(df.loc[i, 'coordinaten'],paden_test.loc[i, 'coordinaten'] )
        
    def test_get_geoposities(self):
        coord_rijbaan = [[51.6841845, 5.2932479], [51.6840109, 5.2936303], [51.6839593, 5.2937284], [51.6839234, 5.2937728], [51.683881, 5.2938087], [51.6838419, 5.2938227], [51.6837928, 5.2938253], [51.6837636, 5.2938189], [51.6837162, 5.2938032], [51.6836028, 5.2937556], [51.6835076, 5.293737], [51.6833894, 5.2937353], [51.6833053, 5.293749], [51.6832155, 5.293777], [51.6831637, 5.2937967], [51.683119, 5.2938207], [51.683119, 5.2938207], [51.6830587, 5.2938612], [51.6829923, 5.293916], [51.6829464, 5.2939591], [51.6828937, 5.2940163], [51.6828124, 5.2941116], [51.6828124, 5.2941116], [51.6827531, 5.2941515], [51.6826961, 5.2941847], [51.6826418, 5.2942023], [51.6825907, 5.2942024], [51.6818223, 5.2940274], [51.6816178, 5.2939892]]
        tree = ET.parse('intersections/BOS210/79190154_BOS210_ITF_COMPLETE.xml')
        df = get_all_lanes_coordinates(tree)
        coordinates = get_geoposities(df, 'RI01E26')
        self.assertEqual(coordinates, coord_rijbaan)
    
    def test_extract_lane_id(self):
        lane1 = '01'
        lane2 = '26'
        l1, l2 = extract_lane_id('RI01E26')
        self.assertEqual([l1,l2], [lane1, lane2])
        
        


