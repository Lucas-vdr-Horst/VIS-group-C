from simulation.classes.Lane import Lane
from simulation.classes.World import World
from simulation.classes.Car import Car
from simulation.classes.Signal import Signal
from simulation.classes.InductionCoil import InductionCoil
from simulation.classes.Location import Location

from preprocess.processing_module import get_coordinates, calculate_trajectory, get_lane, vehicles_laneID
from preprocess.lane_technical_information import get_dict_lane_info
from preprocess.sensor_technical_information import get_dict_sensor_info
from simulation.length_per_laneID import get_length_all_lanes
from common import open_xml
import os
import csv


def run_simulation(begin_time, end_time):
    # hellow there :)

    with open(os.path.join('cars_movements', 'test_car_on_lane.csv'), 'w') as csvfile:
        fieldnames = ['time', 'latitude', 'longitude']
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
        writer.writeheader()

        nodes = ((51.6828358,5.2942547), (51.6827307,5.2942916), (51.6826643,5.2943031), (51.6825965, 5.2943011), (51.6825186, 5.2942849))
        test_lane = Lane('13', nodes, "Ingress")
        test_car = Car(Location(test_lane, test_lane.length-1), 1, 2, False)
        
        t = 1604271611700
        step_size = 100     # miliseconds
        while 0 < test_car.location.meters_from_intersection < test_lane.length:
            car_geo = test_car.location.to_geo()
            writer.writerow({'time': t, 'latitude': car_geo[0], 'longitude': car_geo[1]})
            test_car.move(step_size)
            t += step_size


def run_simulation_reference():
    # This is not runnable at the moment, can be used as reference to code `run_simulation`
    filename = "BOS210" #TODO: temp fix
    root = open_xml(filename)

    # Get dictionary of all vehicle laneID and their lengths
    vehicles_lanes = vehicles_laneID(root) # dict, keys: laneID, value: lanes
    lane_indcoil_signal = get_dict_lane_info(filename) # dictionary of the induction loops and trafficlights of  all lanes
    lanes_length = get_length_all_lanes(filename) #  dictionary of the length of all lanes

    lane_objects = {}

    for id in vehicles_lanes.keys():
        #TODO get signalID of lane if exist, els signalID and signal is None
        if id.zfill(2) in lane_indcoil_signal.keys() and lane_indcoil_signal[id.zfill(2)]['traffic_light'] != '':
            signal_id = lane_indcoil_signal[id.zfill(2)]   #check if id in dict, and get the value of id
            signal = Signal(signal_id['traffic_light'], 'rood')
        else:
            signal = None
        #id: str,length: int,  nodes, signal: Signal(), type_lane

        coordinaten = get_coordinates(root, vehicles_lanes[id], 'ingress')
        length = lanes_length[id.zfill(2)]

        if vehicles_lanes[id][3][0].text == '10':# ingress
            gekoppelde_egresslane = vehicles_lanes[id][5][0][0][0].text
            lane_objects[id] = Lane(id, length, coordinaten,signal,'ingress') # add to dict
            
            #Define the instance variable for a Lane object of a trajectory
            lane_ing = get_lane(root, id)
            traj_id = id+gekoppelde_egresslane # define the id 
            traj_coordinates = get_coordinates(root, lane_ing, 'trajectory') # get coordinates of trajectory 
            traj_length = calculate_trajectory(traj_coordinates[0][1], traj_coordinates[0][0], traj_coordinates[-1][1], traj_coordinates[-1][0]) # calculate the length 
            lane_objects[traj_id] = Lane(traj_id, traj_length, traj_coordinates, None, 'trajectory') # define Lane object and add it ti the dict
            
        else: # egress
            lane_objects[id] = Lane(id, length, coordinaten,signal,'egress')


    # # define a list of Cars objects
    lane1 = lane_objects['1'].getFirstNodes()
    lane26 = lane_objects['26']
    car1 = Car("1",1 , 40,  lane1, lane26) #self, id: str, length: int, speed:int, start_posistion, destination
    cars = [car1]
    
    

    # Get a list of all the Signals 
    n_signals = [Signal(j['traffic_light'], state='rood')  for i, j in lane_indcoil_signal.items() if j['traffic_light'] != '']
    
    #  define a list of InductionCoils objects
    n_inductioncoils= []
    sensors_all_lanes = get_dict_sensor_info(filename)
    for id in lane_objects.keys():
        if lane_objects[id].getTypeLane() != 'trajectory':
            if bool(sensors_all_lanes[id]['sensors']):
                
                # iterate through inductionloops
                for sensorID in sensors_all_lanes[id]['sensors'].keys():
                    centerposition = sensors_all_lanes[id]['sensors'][sensorID]['position']
                    sensor_length = sensors_all_lanes[id]['sensors'][sensorID]['length']
                    induction_coil = InductionCoil(sensorID, centerposition, length, 0)
        
                    # Add to n_inductioncoils
                    n_inductioncoils.append(induction_coil)
                    #set induction_coil to lane
                    lane_objects[id].setInductionloop(induction_coil)
    
    #define een World
    kruispunt = World(1, cars, lane_objects.values(), n_signals, n_inductioncoils, 100.0)
