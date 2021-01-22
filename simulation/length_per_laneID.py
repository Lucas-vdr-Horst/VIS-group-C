import xml.etree.ElementTree as ET
import os
import sys
import collections

sys.path.append('./')
from common import open_xml

from const import intersection_data_location
from preprocess.processing_module import get_lane


def get_length_per_lane(single_lane):
    """
    Get the info of a single lane.

    @params file_name: piece of xml data from a single lane
    @returns: the ID and length of a lane as integer
    """
    lane_id = single_lane[0].text.zfill(2)
    lane_length = single_lane.find('length').text
    return lane_id, lane_length


def get_length_all_lanes(intersection_name):
    """
    Dictionary with length of every lane.

    @param file_name: the name of the xml put in like this -> 'BOS210/79190154_BOS210_ITF_COMPLETE.xml'
    @returns: an dictionary with all length of a lane by laneID
    """

    dict_lanes = {}

    for intersection_name in os.listdir('./intersections'):        
        path = os.path.join('intersections', intersection_name)
        if os.path.isdir(path):
            for xml_file in os.listdir(path):
                if xml_file.endswith('.xml'):
                    xml_file = open_xml(intersection_name)
                    for approachess in xml_file[3][0][7][0][4][0][4]:
                        for approach in approachess:
                            for approach_lane in approach:
                            
                                info_lane = get_length_per_lane(approach_lane)
                                lane_id = info_lane[0]
                                lane = get_lane(xml_file, lane_id)
                                
                                dict_lanes[lane_id] = {'length':info_lane[1]}
    return dict_lanes

