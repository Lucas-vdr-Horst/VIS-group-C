import xml.etree.ElementTree as ET
import os
import sys
from common import open_xml
import collections

sys.path.append('../')

from const import intersection_data_location


def get_length_per_lane(single_lane):
    """
    Get the info of a single lane.

    :param file_name: piece of xml data from a single lane
    :type xml

    :returns: the ID and length of a lane
    :type tuple
    """
    lane_id = single_lane[0].text
    lane_length = single_lane[1].text
    return lane_id, lane_length


def get_length_all_lanes(intersection_name):
    """
    Dictionary with length of every lane.

    :param file_name: the name of the xml put in like this -> 'BOS210/79190154_BOS210_ITF_COMPLETE.xml'
    :type str

    :returns: an dictionary with all length of a lane by laneID
    :type dict
    """
    xml_file = open_xml(intersection_name)

    dict_lanes = {}
    for approachess in xml_file[3][0][7][0][4][0][4]:
        for approach in approachess:
            for approach_lane in approach:
                info_lane = get_length_per_lane(approach_lane)
                lane_id = info_lane[0]
                dict_lanes[lane_id] = info_lane[1]
    return dict_lanes


if __name__ == "__main__":
    print(get_length_all_lanes('BOS210'))