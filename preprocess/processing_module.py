import pandas as pd
import numpy as np
from pathlib import Path
import xml.etree.ElementTree as ET
import os

from math import *
# from lane_technical_information import get_dict_lane_info
import re
from common import get_csv_paths, open_xml, get_xml_path


def get_car_spawn_times(path_to_csv: str, list_of_start_induction_loops: list) -> {"": [""]}:
    """
    This function takes in a csv runtime file and a list of start induction loops to return a dictionary of start
    detection on that loop
    
    @param path_to_csv: file path to csv file
    @param list_of_start_induction_loops: list of induction loops, must be column names in the csv files; example ["02", "12"]
    @return: Dictionary of spawn times from csv file
    """
    list_of_start_induction_loops.insert(0, "time")

    df = pd.read_csv(path_to_csv, sep=';')

    tempfile = path_to_csv + ".temp"

    # Create temp dataframe from selected induction loops and save to temp file
    tempdf = df[list_of_start_induction_loops]
    tempdf = tempdf.set_index('time')
    tempdf.to_csv(tempfile, sep=';')

    # Read though temp csv file and compress file the line to only return lines to list where there are changes
    lst_data = []
    for i, line in enumerate(open(tempfile)):
        if i == 1:
            working_state = line[22:]
            first_time = line[:21]
        elif i > 0:
            state = line[22:]
            time = line[:21]
            if working_state != state:
                test_string = (f"{first_time};{working_state}".rstrip("\n"))
                if "|" in test_string:
                    lst_data.append(test_string.split(";"))
                working_state = state
                first_time = time
    test_string = (f"{first_time};{working_state}".rstrip("\n"))
    if "|" in test_string:
        lst_data.append(test_string.split(";"))

    tempdf = tempdf.reset_index()
    
    # Create new df with the compresed lines and filter out uninterested rows
    df_new = pd.DataFrame(lst_data, columns=tempdf.columns)
    df_new = df_new[list_of_start_induction_loops]
    df_new = df_new.replace("", np.nan)
    df_new = df_new.dropna(thresh=2)

    # Formate to dict for structure
    return_dict = {}
    for c in list_of_start_induction_loops[1:]:
        return_dict[c] = df_new[[list_of_start_induction_loops[0], c]].loc[df_new[c] == "|"]['time'].values.tolist()

    # Delete temporary file
    if os.path.exists(tempfile):
        os.remove(tempfile)

    return return_dict


def calculate_trajectory(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance of a trajectory based on 2 coordinates.

    @params lon1, lat1: Coordinate  1
    @params lon2, lat2: Coordinate  2
    @return distance between coordinate 1 and 2 

    """
    # zet de coordinaten om naar radialen
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    distance = c * r

    return distance


# Function to get the necessary laneID for the simulation 
def vehicles_laneID(root) -> dict:
    """
    Get all laneID of all lanes specifically to vehicles and update the to a dictionary.
    
    @params root
    @returns: Dictionary of laneID's of all vehicle lanes from XML file 
    """
    laneSet = root[2][1][0][6]
    vehicles = {}
    for  i in laneSet: # iterate through LaneSet
        if i[3][2].tag == 'vehicle': # check if lane is for vehicles
            vehicles[i.find('laneID').text] = i # add laneID and lane to dict
    return vehicles


def get_nodes(nodes):
    """
    Get the coordinates in a nodes  of a lane.

    @params nodes : Element from XML file containing the coordinates in (long, lat)
    @returns: Nested list of all the converted coordinates [lat,lon] of lane
    """
    coordinates = []
    for node in nodes:
        for n in node.iter('node-LatLon'):  # node.iter('node-LatLon') == node-latlon # iterating through node-LatLon
            # Convert the longitude and latitude to an integer and divided by 10000000 (deciml degrees) 
            lon = int(n.findall('lon')[0].text) / 10000000
            lat = int(n.findall('lat')[0].text) / 10000000
            coordinates.append([lat, lon])  # add coordinates to list
    return coordinates


def get_lane(root, laneID):
    """
    Get the genericlane Element of a specific laneID from the XML file.
    
    @params root
    @params LaneID: String of the given laneID
    """
    laneSet = root[2][1][0][6]
    for lane in laneSet: 
        if lane[0].text == laneID: # check if laneID from lane is equal to our input laneID
            lane = lane
            break
    return lane


def get_coordinates(root, lane, type_lane):
    """
    Get the coordinates of a lanes/trajectory.

    @params root
    @params laneID: laneID of an ingress or egresslane
    @params type_lane: A string where is given whether lane is an ingress, egress or a trajectory.
    @returns: Nested list with the coordinates of a lanes/trajectory.
    """
    # lane = get_lane(root, laneID)
    # In order to get the coordinates of the trajectory,
    if type_lane == 'trajectory':
        # get the coordinates of nodes in lane 
        coordinates = get_nodes(lane[6][0][0])
    else:  # type_lane == ingress or egress
        coordinates = get_nodes(lane[4])
    return coordinates

