import sys

sys.path.append('./')

from common import open_xml


def get_lane_nodes(xml_file) -> dict:
    """
    This function returns all nodes af a single lane.
    @param xml_file: the whole xml_file of all intersections
    @return: a dictionary with all the nodes per lane
    """
    dict_nodes_lane = {}
    lane_set = xml_file[2][1][0][6] # topology/mapData/intersections/laneset
    for generic_lane in lane_set:
        lane_id = generic_lane.find('laneID').text    
        list_with_coordinates = []
        for nodeXY in generic_lane[4]:
            lat = int(nodeXY[0].find('lat').text) / 10000000
            lon = int(nodeXY[0].find('lon').text) / 10000000
            list_with_coordinates.append([lat, lon])
        dict_nodes_lane[lane_id] = list_with_coordinates

    return dict_nodes_lane


def get_induction_loop_data(xml_file) -> dict:
    """
    Get per lane information about the inductioncoil names, the centerpositions, the lengths.
    @param xml_file: the whole xml file
    @return: Dictionary with info about all sensors per lane
    """
    sensors = xml_file[3][0][7][0][4][0][5] #topology/controlData/controller/controlUnits/controlUnit/controlledIntersections/controlledIntersection/sensors
    sensor_dict = {}
    
    for sensor in sensors:
        try:
            sensor_length = sensor.find('length').text
            sensor_name = sensor.find('name').text
            sensor_position = [sensor[5].find('lat').text, sensor[5].find('long').text]
            lane_id_sensor = sensor[8][0].find('laneID').text
            sensor_dict[sensor_name] = {'position': sensor_position, 'length': sensor_length, 'located_on_laneID': lane_id_sensor}
        except:
            continue
    return sensor_dict

def get_dict_sensor_info(file_name) -> dict:
    """
    Makes a dict with the induction loops and trafficlights of a lane. Keys are presented in string.
    @param file_name: the locationname of the CSV put in like this -> 'BOS210'
    @returns: all technical info of sensors per lane in a dictionary
    """

    xml_file = open_xml(file_name)
    sensor_information_dict = get_induction_loop_data(xml_file)
    new_dict = {}
    nodes_lanes_info = get_lane_nodes(xml_file)
    for lane_id, nodes in nodes_lanes_info.items():
        sensor_info = {}
        for sensor in sensor_information_dict:
            if sensor_information_dict[sensor]['located_on_laneID'] == lane_id:
                if sensor in sensor_info:
                    sensor_info[sensor].append(sensor_information_dict[sensor])
                else:
                    sensor_info[sensor] = sensor_information_dict[sensor]
        new_dict[lane_id] = {'first_node_lane_id' : nodes[0], 'sensors':sensor_info}
    return new_dict

if __name__ == "__main__":
    for i, j in get_dict_sensor_info("BOS210").items():
        print(i)
        print(j)
    #print(get_dict_sensor_info("BOS210"))