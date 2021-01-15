from simulation.classes.Lane import Lane
from simulation.classes.World import World
from simulation.classes.Car import Car
from simulation.classes.Signal import Signal
from simulation.classes.InductionCoil import InductionCoil
import os
import sys
from preprocess.processing_module import get_coordinates, calculate_trajectory
from preprocess.lane_technical_information import get_dict_lane_info
from simulation.length_per_laneID import get_length_all_lanes
from common import open_xml

def run_simulation(filename):
    print('do simulation. beep. boop.')
    root = open_xml('BOS210')

    # Get dictionary of all vehicle laneID and their lengths
    lane_indcoil_signal = get_dict_lane_info(filename)
    
    lanes = get_length_all_lanes(filename)
    for id in lanes.keys():
        if lanes[id]['lane'][3][0].text == '10':# ingress
            signal_id = lane_indcoil_signal[id]['traffic_lights']
            signal = Signal(signal_id, 'rood')
            #id: str,length: int,  nodes, signal: Signal(), type_lane
            coordinaten = get_coordinates(root, lanes[id]['lane'], 'ingress')
            length = lanes[id]['length']
            lanes[id] = Lane(id, length, coordinaten,signal,'ingress')
    
    [print(i, j) for i,j in lanes.item()]

    # # define a list of Cars objects
    # #self, id: str, length: int, speed:int, start_posistion, destination
    # lane1 = lanes['1'].getNodes()
    # lane26 = lanes['26']
    # car1 = Car("1", 1, 40,  lane1[0], lane26)
    # cars = [car1]

    # # get n_signals
    # signals_ids =[j['traffic_lights'].values() for _, j in  lane_indcoil_signal.items()]
    # n_signals = [Signal(i, state='rood') for i in signals_ids]
 
    # # define a list of InductionCoils objects 

    # # define een World
    # kruispunt = World(1, cars, lanes.values())#, n_signals:list, n_inductioncoils:list, runtime: float)
