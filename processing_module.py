import pandas as pd
import numpy as np
from pathlib import Path
from data_cleaning import fix_hashtags
import xml.etree.ElementTree as ET
import json
import os
from math import *


def calculate_markers_points(lat1: float, lon1: float, lat2: float, lon2: float, marker_count: int) -> [[float, float]]:
    """
    Deze functie heeft 2 geo locaties nodig en geeft een lijst met geo locaties ertussen terug
    @param marker_count: Aantal markers over de conflict zone
    @param lat1: Latitude van geo 1
    @param lon1: longitude van geo 1
    @param lat2: Latitude van geo 2
    @param lon2: longitude van geo 2
    @return: list van geo locations tussen 2 geolocaties
    """
    # Todo deze functie maakt nu alleen nog maar een rechtelijn, moet veranderd worden naar iets met een curve
    lat = np.linspace(lat1, lat2, num=marker_count)
    lon = np.linspace(lon1, lon2, num=marker_count)
    #coordinates = list(zip(lat, lon))
    coordinates = list(map(list, zip(lat, lon)))

    return coordinates


def calculate_trajectory(lon1, lat1, lon2, lat2):
    # zet de coordinaten om naar radialen
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    distance = c * r

    # calculate the bearing
    bearing = atan2(cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(lon2 - lon1), sin(lon2 - lon1) * cos(lat2))
    return distance, bearing


def deg2rad(angle):
    return angle * pi / 180

def rad2deg(angle):
    return angle * 180 / pi


def pointRadialDistance(lat1, lon1, bearing, distance):
    """
    Return final coordinates (lat2,lon2) [in degrees] given initial coordinates
    (lat1,lon1) [in degrees] and a bearing [in degrees] and distance [in km]
    """
    rEarth = 6371.01  # Earth's average radius in km
    epsilon = 0.000001  # threshold for floating-point equality
    rlat1 = deg2rad(lat1)
    rlon1 = deg2rad(lon1)
    rbearing = deg2rad(bearing)
    rdistance = distance / rEarth  # normalize linear distance to radian angle

    rlat = asin(sin(rlat1) * cos(rdistance) + cos(rlat1) * sin(rdistance) * cos(rbearing))

    if cos(rlat) == 0 or abs(cos(rlat)) < epsilon:  # Endpoint a pole
        rlon = rlon1
    else:
        rlon = ((rlon1 - asin(sin(rbearing) * sin(rdistance) / cos(rlat)) + pi) % (2 * pi)) - pi

    lat = rad2deg(rlat)
    lon = rad2deg(rlon)
    return lon, lat


def load_sensor_data(begin_time, end_time):
    # df_sensor = pd.read_csv(os.path.join(intersection_data_location, intersection_name, '*.csv'), delimiter=";", low_memory=False)
    df_sensor = pd.read_csv("intersections/BOS210/BOS210.csv", delimiter=";", dtype=str)
    df_sensor = df_sensor.set_index('time')  # set index to time
    data_sensor_specific_time = df_sensor.loc[begin_time:end_time]  # filter to begin and end time
    return data_sensor_specific_time


def get_coordinates_lane(genericlane):
    """
    Extract all longitude en latitude of a specific lane
    
    :param genericlane: a variable what contains 1 lane
    :type xml

    :returns coordinates: all coordinates of a lane
    :type list
    """
    coordinates = []
    for node in genericlane.iter('nodes'):  # i.iter('nodes') == nodes
        for n in node.iter('node-LatLon'):  # node.iter('node-LatLon') == node-latlon
            lon = int(n.findall('lon')[0].text)
            lat = int(n.findall('lat')[0].text)
            coordinates.append([lon, lat])
    return coordinates


def json_file_all_lanes_coordinates(tree):
    """
    Returns a Json file with the coordinates of all lanes.

    :param tree: info about the intersections
    :type xml

    :returns: file with all coordinates from all lanes
    :type json
    """
    root = tree.getroot()
    dict_with_coords = {}
    laneSet = root[2][1][0][6]
    for genericlane in laneSet:  # iterate through laneset
        if genericlane[3][2].tag == 'vehicle' and genericlane[
            2].tag == 'ingressApproach':  # pak de ingress lanes van  auto's
            laneId = int(genericlane.find('laneID').text)  # haal uit laneId
            connected_to = genericlane[5][0][0][0].text

            for lane in laneSet:
                if lane[0].text == connected_to:
                    connected_to_lane = lane

            coordinaten_lane_in = get_coordinates_lane(genericlane)
            coordinaten_lane_out = get_coordinates_lane(connected_to_lane)
            lon1, lat1 = [i / 10000000 for i in
                          coordinaten_lane_in[0]]  # pakt de eerste coordinaten van de ingress lane
            lon2, lat2 = [i / 10000000 for i in
                          coordinaten_lane_out[0]]  # pakt de eerste coordinaten van de egress lane

            distance, bearing = calculate_trajectory(lon1, lat1, lon2, lat2)

            print("Distance: {}, bearing:{}".format(distance * 1000, bearing))
            print("Lane {} :lon1: {}, lat1: {}; Lane{} :lon2:{}, lat2:{}".format(laneId, lon1, lat1, connected_to, lon2,
                                                                                 lat2))
            print("Calculated lon and lat: {}".format(pointRadialDistance(lat1, lon1, bearing, distance)))
            print("\n")

            # numsteps = 5
            # coord = np.zeros([numsteps+1, 2])
            # coord[0][0] = lon1
            # coord[0][1] = lat1
            # for step  in range(numsteps):
            #     coord[step+1] = pointRadialDistance( coord[step][0], coord[step][1], (distance*1000)/5, bearing/5)
            # print(coord)
            # print("\n")

        dict_with_coords[laneId] = coordinaten_lane_in + coordinaten_lane_out

    json_file = json.dumps(dict_with_coords)
    return json_file


def process(begin_time, end_time):
    """
    Returns a Json file.

    :param begin_time: Datetime dd-mm-yyyy hh:mm:ss:m starttime
    :type Datetime

    :param end_time: Datetime dd-mm-yyyy hh:mm:ss:m endtime
    :type Datetime
    """

    sensor_data = load_sensor_data(begin_time, end_time)

    tree = ET.parse('intersections/BOS210/79190154_BOS210_ITF_COMPLETE.xml')
    json_file = json_file_all_lanes_coordinates(tree)

    # TODO: voor iedere rij in sensordata check of sensor geraakt wordt. wanneer een sensor geraakt wordt zoek welke lane deze sensor zit en voeg de coordinaten voor die lane toe aan returnvalue

    # return een file met alle auto's die rijden op dat moment

    return json_file


if __name__ == "__main__":
    process("02-11-2020 00:00:00.0", "02-11-2020 00:00:00.6")

# [     long       lat         long     lat       long      lat
#   [[378328794, 4893289004], [893924, 483724], [48328094, 38492043]],  auto1
#   [[378328794, 4893289004], [893924, 483724], [48328094, 38492043]],  auto2
#   [[378328794, 4893289004], [893924, 483724], [48328094, 38492043]]   auto3
# ]

# RI16E20 :=   Lane 16 -> Calculated Trajectory -> Lane 20
# RI16E20 :=   IngressLane -> Calculated Trajectory -> Exgresslane
# RI16E20 :=   [[float , float],[float , float]]
#
# R       I      E
# Rijbaan Ingres Exgress
