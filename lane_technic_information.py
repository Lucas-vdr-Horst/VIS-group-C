import xml.etree.ElementTree as ET


def open_xml():
    tree = ET.parse('intersections/BOS210/79190154_BOS210_ITF_COMPLETE.xml')
    root = tree.getroot()
    return root


def get_signalGroup_from_lane(laneID, root):
    laneSet = root[2][1][0][6] # topology/mapData/intersections/laneset
    for genericlane in laneSet:
        if genericlane[0].text == laneID:
            return genericlane[5][0][2].text


def get_trafficsignal_name(signalgroupnumber, root):
    signalgroups = root[3][0][7][0][4][0][7] #topology/controlData/controller/controlUnits/controlUnit/controlledIntersections/controlledIntersection/sensors
    for signalgroup in signalgroups:
        if signalgroup[0].text == signalgroupnumber:
            return signalgroup[0].text
            


def get_dict_lane_info():
    """
    Returns a dict with the induction loops and trafficlights of a lane. Keys are Str

    :returns: file with all coordinates from all lanes
    :type csv
    """
    xml_file = open_xml()
    dict_info_lanes = {}
    sensors = xml_file[3][0][7][0][4][0][5] #topology/controlData/controller/controlUnits/controlUnit/controlledIntersections/controlledIntersection/sensors
    for sensor in sensors:
        try:
            laneID = sensor[8][0][0].text
        except:
            break

        if laneID not in dict_info_lanes:
            dict_info_lanes[laneID] = {'induction_loops': [], 'traffic_light': ''}
        sensor_name = (sensor[1].text)
        dict_info_lanes[laneID]['induction_loops'].append(sensor_name)
        signal_group = get_signalGroup_from_lane(laneID, xml_file)
        traffic_light = get_trafficsignal_name(signal_group, xml_file)
        dict_info_lanes[laneID]['traffic_light'] = traffic_light
    return dict_info_lanes


if __name__ == "__main__":
    dict_with_info = get_dict_lane_info()
    print(dict_with_info['1'])