import xml.etree.ElementTree as ET

import sys
sys.path.append('./')

from common import open_xml


def get_signalGroup_from_lane(laneID, root) -> str:
    """
    Get the signalgroup name connected to a lane.

    @params laneID: laneID of the specific lane
    @params root: the xml file of an intersection
    @returns: a string with the signalgroupname of a specific lane
    """
    laneSet = root[2][1][0][6] # topology/mapData/intersections/laneset
    for genericlane in laneSet:
        if genericlane[0].text == laneID:
            try:
                signalgroup = genericlane[5][0][1].text

            except:
                signalgroup = None

            return signalgroup


def get_trafficsignal_name(signalgroupnumber, root) -> str:
    """
    Get the trafficlight name that correspons to a signalgroupnumber

    @params signalgroupnumber: an integer number that represents the signalgroupnumber
    @params root: the xml file of an intersection
    @returns: a string with the name of a trafficlight
    """
    signalgroups = root[3][0][7][0][4][0][6]  # topology/controlData/controller/controlUnits/controlUnit/controlledIntersections/controlledIntersection/sensors
    for signalgroup in signalgroups:
        if signalgroup[1].text == str(signalgroupnumber):
            return signalgroup[0].text


def get_dict_lane_info(file_name)-> dict:
    """
    Makes a dict with the induction loops and trafficlights of a lane. Keys are presented in string.

    @param file_name: the directoryname where the xml are put in
    @returns: all technical info of a lane in a dictionary
    """

    xml_file = open_xml(file_name)
    dict_info_lanes = {}
    sensors = xml_file[3][0][7][0][4][0][5] #topology/controlData/controller/controlUnits/controlUnit/controlledIntersections/controlledIntersection/sensors
    for sensor in sensors:
        try:
            laneID = (sensor[8][0][0].text).zfill(2)
        except:
            continue

        if laneID not in dict_info_lanes:
            dict_info_lanes[laneID] = {'induction_loops': [], 'traffic_light': ''}
        sensor_name = (sensor[1].text)
        dict_info_lanes[laneID]['induction_loops'].append(sensor_name)
        signal_group = get_signalGroup_from_lane(laneID, xml_file)
        if signal_group != None:
            traffic_light = get_trafficsignal_name(signal_group, xml_file)
            dict_info_lanes[laneID]['traffic_light'] = traffic_light
    return dict_info_lanes


if __name__ == "__main__":
    dict_with_info = get_dict_lane_info('BOS210')
    print(dict_with_info)