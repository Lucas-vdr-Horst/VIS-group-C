import sys

sys.path.append('./')

from common import open_xml


def get_lane_nodes(xml_file):
    dict_nodes_per_lane = {}
    lane_set = xml_file[2][1][0][6] # topology/mapData/intersections/laneset
    for generic_lane in lane_set:
        lane_id = generic_lane.find('laneID').text    
        list_with_coordinates = []
        for nodeXY in generic_lane[4]:
            lat = int(nodeXY[0].find('lat').text) / 10000000
            lon = int(nodeXY[0].find('lon').text) / 10000000
            list_with_coordinates.append([lat, lon])
        dict_nodes_per_lane[lane_id] = list_with_coordinates

    return get_lane_nodes


def get_induction_loop_data(xml_file):
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

def get_dict_sensor_info(file_name):
    """
    Makes a dict with the induction loops and trafficlights of a lane. Keys are presented in string.
    
    :param file_name: the locationname of the CSV put in like this -> 'BOS210/79190154_BOS210_ITF_COMPLETE.xml'
    :type str

    :returns: all technical info of a lane
    :type dict
    """

    xml_file = open_xml(file_name)
    dict_info_lanes = {}
    nodes_lanes_info = get_lane_nodes(xml_file)

    sensor_information_dict = get_induction_loop_data(xml_file)


    
if __name__ == "__main__":
    #dict_with_info = get_dict_lane_info('BOS210')
    #print(dict_with_info)
    print(get_dict_sensor_info("BOS210"))