import xml.etree.ElementTree as ET
from common import open_xml

def get_laneID_of_sensor(root):
    sensors = root[3][0][7][0][4][0][5] #topology/controlData/controller/controlUnits/controlUnit/controlledIntersections/controlledIntersection/sensors
    for sensor in sensors:
        if sensor[1].text == 'sensor_name':
            return sensor[8][0][0] # sensorAllocations/sensorAllocation/laneID


def get_trafficsignal_name(signalgroupnumber, root):
    signalgroups = root[3][0][7][0][4][0][7] #topology/controlData/controller/controlUnits/controlUnit/controlledIntersections/controlledIntersection/sensors
    for signalgroup in signalgroups:
        print(signalgroup)
        if signalgroup[0] == signalgroupnumber:
            return signalgroup[0]


def check_laneID(signalgroup, root):
    laneSet = root[2][1][0][6] # topology/mapData/intersections/laneset
    for genericlane in laneSet:
        pass #print(genericlane[0])


def calculate_avg_waitingtime(file_name):
    """Calculates avg time of trafficlight waiting time"""
    xml_file = open_xml(file_name)

    # TODO check csv for data pressed inductionloops

    sensor_name = ["124"]
    laneID = get_laneID_of_sensor(sensor_name, xml_file)


if __name__ == "__main__":
    file_name = "BOS210"
    calculate_avg_waitingtime(file_name)

