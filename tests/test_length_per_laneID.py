from unittest import TestCase

import sys

sys.path.append('./')
from common import open_xml
from simulation.length_per_laneID import get_length_per_lane, get_length_all_lanes


class Test(TestCase):

    def test_get_length_per_lane(self):
        xml_file = open_xml("BOS210")
        lane = xml_file[3][0][7][0][4][0][4][0][2][0]
        expected_output = ("01", "1380")
        output_file = get_length_per_lane(lane)

        self.assertEqual(output_file, expected_output)

    def test_get_length_all_lanes(self):
        intersection_name = "BOS210"
        length_all_lanes = get_length_all_lanes(intersection_name)
        expected_output = {'01': {'length': '893'}, '02': {'length': '997'}, '05': {'length': '25'}, '06': {'length': '22'}, '15': {'length': '1526'}, '17': {'length': '867'}, '18': {'length': '863'}, '21': {'length': '1295'}, '22': {'length': '1400'}, '07': {'length': '1352'}, '08': {'length': '65535'}, '10': {'length': '7'}, '11': {'length': '20'}, '12': {'length': '13'}, '19': {'length': '65535'}, '20': {'length': '1319'}, '24': {'length': '18'}, '25': {'length': '65535'}, '13': {'length': '582'}, '14': {'length': '1542'}, '26': {'length': '11'}, '04': {'length': '2008'}, '23': {'length': '23'},
'29': {'length': '65535'}, '30': {'length': '65535'}, '09': {'length': '79'}, '03': {'length': '993'}, '27': {'length': '23'}, '28': {'length': '19'}, '16': {'length': '1098'}}
        self.assertEqual(length_all_lanes, expected_output)