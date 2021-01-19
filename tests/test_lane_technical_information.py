from unittest import TestCase
import xml.etree.ElementTree as ET
import sys
sys.path.append('./')

from common import open_xml
from preprocess.lane_technical_information import get_dict_lane_info, get_trafficsignal_name, get_signalGroup_from_lane

class Test(TestCase):

    def test_get_dict_lane_info(self):
        file_name = 'BOS210'
        expected_output = {'07': {'induction_loops': ['011', '012', '013', '014'], 'traffic_light': ''}, '08': {'induction_loops': ['031', '032', '033', '034'], 'traffic_light': ''}, '13': {'induction_loops': ['041', '042', '043', '044'], 'traffic_light': '3'}, '14': {'induction_loops': ['051', '052', '053', '054'], 'traffic_light': '4'}, '01': {'induction_loops': ['111', '112', '113', '114'], 'traffic_light': ''}, '02': {'induction_loops': ['121', '122', '123', '124'], 'traffic_light': ''}, '09': {'induction_loops': ['221', '222', '223'], 'traffic_light': ''}, '03': {'induction_loops': ['241'], 'traffic_light': ''}, '04': {'induction_loops': ['281'], 'traffic_light': ''}, '12': {'induction_loops': ['411', '412'], 'traffic_light': '14'}, '15': {'induction_loops': ['F055'], 'traffic_light': ''}}

        output_file = get_dict_lane_info(file_name)
        
        self.assertEqual(output_file, expected_output)
    
    def test_get_trafficsignal_name(self):
        signalgroupnumber = 1
        root = open_xml('BOS210')

        name_traffic_signal = get_trafficsignal_name(signalgroupnumber, root)
        expected_output = '01'

        self.assertEqual(name_traffic_signal, expected_output)

    def get_signalGroup_from_lane(self):
        laneID = 1
        root = open_xml('BOS210')

        signal_group_name = get_signalGroup_from_lane(laneID, root)
        expected_output = 13

        self.assertEqual(signal_group_name, expected_output)

    
