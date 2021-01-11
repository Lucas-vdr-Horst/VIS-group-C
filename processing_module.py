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
    distance, bearing = calculate_trajectory(lon1, lat1, lon2, lat2)

    angle = bearing - 90
    if angle < 0 :
        angle +=  360
    elif angle > 360:
        angle -= 360
    print(angle)

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
    return lat, lon


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

    :returns coordinates: all coordinates of a lane - [[lat, lon],..]
    :type list
    """
    lane_coord = []
    lane_nodes = genericlane[4] 
    for node in lane_nodes: # Iterate through nodes of genericlane
        for n in node.iter('node-LatLon'):  # node.iter('node-LatLon') == node-latlon # iterating through node-LatLon
            # Convert the longitude and latitude to an integer and divided by 10000000 (deciml degrees) 
            lon = int(n.findall('lon')[0].text)/10000000 
            lat = int(n.findall('lat')[0].text)/10000000 
            lane_coord.append([lat,lon])  # add coordinates to list 
    
    if genericlane[2].tag == 'ingressApproach': # check if lane is ingress or egress
        trajectory_coord = []
        regional = genericlane[6][0][0]
        for  node in regional: # iterate through nodes in regional 
            for n in node.iter('node-LatLon'):  # node.iter('node-LatLon') == node-latlon
                lon = int(n.findall('lon')[0].text)/10000000
                lat = int(n.findall('lat')[0].text)/10000000
                trajectory_coord.append([lat,lon])
        # If lane is ingress, the list lane_coord has to be reversed
        lane_coord =lane_coord[::-1] 
        coordinaten = lane_coord + trajectory_coord # concatenate lane_coord and trajectory_coord
    else:
        coordinaten = lane_coord
    return coordinaten


def get_all_lanes_coordinates(tree):
    """
    Returns a CSV file with the coordinates of all lanes.

    :param tree: info about the intersections
    :type xml

    :returns: file with all coordinates from all lanes
    :type csv
    """
    paden_auto = pd.DataFrame(columns = ['Rijbaan', 'coordinaten']) #'ingress_coordinaten', 'trajectory_coordinaten', 'egress_coordinaten']) # create dataframe that wil contains the coordinates from all lanes
    
    root = tree.getroot()

    laneSet = root[2][1][0][6]
    for genericlane in laneSet:  # iterate through laneset
        if genericlane[3][2].tag == 'vehicle' and genericlane[2].tag == 'ingressApproach':  # pak de ingress lanes van  auto's
            laneId = int(genericlane.find('laneID').text)  # haal uit laneID van de ingresslane
            connected_to = genericlane[5][0][0][0].text   # haal uit de laneID van de gekoppelde egresslane

            #Haal uit de genericlane element van de egresslane
            for lane in laneSet:
                if lane[0].text == connected_to:
                    connected_to_lane = lane

            coordinaten_lane_in = get_coordinates_lane(genericlane) # coordinaten van de ingresslane
            coordinaten_lane_out = get_coordinates_lane(connected_to_lane) # coordinaten van de egresslane
            # print("Lane {} : {}".format(connected_to, coordinaten_lane_out))
            # print("genericlane {}: {}".format(connected_to,connected_to_lane))
            # print("\n")
            #paden_auto = paden_auto.append({'Rijbaan' : laneId , 'ingress_coordinaten' : coordinaten_lane_in,'trajectory_coordinaten' : coordinaten_trajectory,'egress_coordinaten' : coordinaten_lane_out} , ignore_index=True)
            
            #Voeg coordinaten toe in dataframe
            rijbaan = 'RI{}E{}'.format(laneId, connected_to)
            paden_auto = paden_auto.append({'Rijbaan': rijbaan , 'coordinaten' : coordinaten_lane_in +coordinaten_lane_out} , ignore_index=True)
            
    return paden_auto


def process():
    """
    Returns a csv file with the coordinates of riding track for a vehicle
    """
    tree = ET.parse('intersections/BOS210/79190154_BOS210_ITF_COMPLETE.xml') # parse given XML file
    paden = get_all_lanes_coordinates(tree) # get dataframe with the coordinates of all lanes
    print(paden['coordinaten'])
    #csv_paden  = paden.to_csv('paden_autos',index=False) # convert dataframe to csv

    return paden
    


if __name__ == "__main__":
    #process("02-11-2020 00:00:00.0", "02-11-2020 00:00:00.6")
    process()
