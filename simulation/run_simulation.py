from simulation.classes.Lane import Lane
from simulation.classes.World import World
from simulation.classes.Car import Car
from simulation.classes.Signal import Signal
from simulation.classes.InductionCoil import InductionCoil
from simulation.classes.Location import Location

from preprocess.processing_module import get_coordinates, calculate_trajectory, get_lane
from preprocess.lane_technical_information import get_dict_lane_info
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
    lane_indcoil_signal = get_dict_lane_info(filename)
    lanes = get_length_all_lanes(filename)
    lane_objects = {}
    for id in lanes.keys():
        #TODO get signalID of lane if exist, els signalID and signal is None
        signal_id = lane_indcoil_signal[id.zfill(2)] if id.zfill(2) in lane_indcoil_signal.keys()   else '' # check if id in dict
        signal = Signal(signal_id, 'rood') if signal_id != '' else None
        #id: str,length: int,  nodes, signal: Signal(), type_lane
        coordinaten = get_coordinates(root, lanes[id]['lane'], 'ingress')
        length = lanes[id]['length']
        if lanes[id]['lane'][3][0].text == '10':# ingress
            gekoppelde_egresslane = lanes[id]['lane'][5][0][0][0].text
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
    lane1 = lane_objects['13'].getNodes()
    lane26 = lane_objects['19']
    car1 = Car("1",1 , 40,  lane1[0], lane26) #self, id: str, length: int, speed:int, start_posistion, destination
    cars = [car1]
    

    #  get n_signals
    n_signals = [Signal(j['traffic_light'], state='rood') for i, j in lane_indcoil_signal.items()]
    #  define a list of InductionCoils objects 
    # loc = Location('1', '13')
    # ind1 = InductionCoil( 1, loc, )


    # # define een World
    # #kruispunt = World(1, cars, lanes.values())#, n_signals:list, n_inductioncoils:list, runtime: float)
