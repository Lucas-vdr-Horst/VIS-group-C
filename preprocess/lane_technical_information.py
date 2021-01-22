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
                signalgroup = genericlane[5][0][1].text # get the id of the traffic Light of lane

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
            laneID = (sensor[8][0][0].text).zfill(2) # get the laneID where sensor is located
        except:
            continue

        if laneID not in dict_info_lanes: # check if laneID is not already in dict
            dict_info_lanes[laneID] = {'induction_loops': [], 'traffic_light': ''}
        sensor_name = (sensor[1].text) # get sensorID of sensor
        dict_info_lanes[laneID]['induction_loops'].append(sensor_name) # add sensorID to list induction_loops in dict 
        signal_group = get_signalGroup_from_lane(laneID, xml_file) #get signalGroup
        if signal_group != None:
            traffic_light = get_trafficsignal_name(signal_group, xml_file) # get trafficsignal name 
            dict_info_lanes[laneID]['traffic_light'] = traffic_light # traffic_light name to dict of laneID
    return dict_info_lanes