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
from common import open_xml, get_available_intersections
from const import cars_data_location
import os
import csv
import glob
import names
from alive_progress import alive_bar


def run_simulation(begin_time, end_time):
    # hellow there :)

    run_test_simulation(begin_time, end_time)
    #run_simulation_reference()
    #run_simulation_merge()


def run_test_simulation(begin_time, end_time):
    lanes, signals, inductioncoils = load_lanes_signals_and_inductioncoils()
    worlds = []
    car_merges = []
    to_update = []

    # Initialize worlds with car spawn points
    with open(os.path.join('preprocess', 'output', 'spawn_points.csv')) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)
        for i, row in enumerate(reader):
            car = Car(i, Location(lanes[row[1]], float(row[2])), 2.0, 5.0)
            time = int(row[0])
            world = World([car], lanes, signals, inductioncoils, time)
            worlds.append(world)
            car_merges.append({'ids': [car.id], 'first_time': time, 'last_time': time})
            to_update.append(world)
    
    # Main simulation loop
    while to_update:
        to_update.pop()
        # TODO

    # Write to csv's
    claimed_names = set(map(lambda x: x.replace(cars_data_location, '').replace('.csv', ''), glob.glob(os.path.join(cars_data_location, '*.csv'))))
    # Take a look at this in the morning with a fresh mind. car -> world or world -> car?
    for merge in car_merges:
        car_name = names.get_full_name().replace(' ', '')
        while car_name in claimed_names:
            car_name = car_name + 'Jr.'
        claimed_names.add(car_name)

        with open(os.path.join(cars_data_location, f"{car_name}.csv"), 'w') as file:
            writer = csv.writer(file, delimiter=';', lineterminator='\n')
            writer.writerow(('time', 'latitude', 'longitude'))
            for world in worlds:
                if world.runtime >= merge['first_time']:
                    if world.runtime <= merge['last_time']:
                        # get the right car and write this one to csv
                        #car = world.
                        writer.writerow(())
                    else:
                        break

    
# 'testCar' + car.location.lane.id + world.runtime.toString()

    # with open(os.path.join('cars_movements', 'test_car_on_lane.csv'), 'w') as csvfile:
    #     fieldnames = ['time', 'latitude', 'longitude']
    #     writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames, lineterminator='\n')
    #     writer.writeheader()

    #     nodes = ((51.6828358, 5.2942547), (51.6827307, 5.2942916), (51.6826643, 5.2943031), (51.6825965, 5.2943011),
    #              (51.6825186, 5.2942849))
    #     test_lane = Lane('13', nodes, "Ingress")
    #     test_car = Car('0', Location(test_lane, test_lane.length - 1), 1, 2, False)

    #     t = 1604271611700
    #     step_size = 100  # miliseconds
    #     while 0 < test_car.location.meters_from_intersection < test_lane.length:
    #         car_geo = test_car.location.to_geo()
    #         writer.writerow({'time': t, 'latitude': car_geo[0], 'longitude': car_geo[1]})
    #         test_car.move(step_size, None)
    #         t += step_size

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
            linked_egresslane = vehicles_lanes[id][5][0][0][0].text
            lane_objects[id] = Lane(id, length, coordinaten,signal,'ingress') # add to dict
            
            #Define the instance variable for a Lane object of a trajectory
            lane_ing = get_lane(root, id)
            traj_id = id+linked_egresslane # define the id 
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

def get_lane_objects(vehicles_lanes, lane_indcoil_signal, root) -> dict:
    """
    Return a list containing defined Lane objects of all the vehicle lanes in specified filename

    For our simulation, we will be focusing on the lane that is intended for a vehicle.
    """
    lane_objects = {} # list containing the Lane Objects

    for id in vehicles_lanes.keys():# iterate through each  lane

        # Defining Signal object of  lane
        if id.zfill(2) in lane_indcoil_signal.keys() and lane_indcoil_signal[id.zfill(2)]['traffic_light'] != '': # check if laneID of  lane in dict and if  lane contains any traffic lights
            signal_id = lane_indcoil_signal[id.zfill(2)]['traffic_light'] # get the signal_id 
            
            signal = Signal(signal_id) # define Signal object
        else:
            signal = None

        coordinaten = get_coordinates(root, vehicles_lanes[id], 'ingress')#[::-1] # get the coordinates of  lane

        #Define Lane object based on the type of the lane.
        # An ingresslane contains the necessary coordinates of an trajectory. 
        # We can directly define an trajectory Lane object and an ingress Lane object. 
        if vehicles_lanes[id][3][0].text == '10':  # ingress
            linked_egresslane = vehicles_lanes[id][5][0][0][0].text
            
            lane_objects[id] = Lane(id, coordinaten, 'ingress', signal)  # add to dict

            # Define the instance variable for a Lane object of a trajectory
            lane_ing = get_lane(root, id)
            traj_id = id + '-' + linked_egresslane  # define the id
            traj_coordinates = get_coordinates(root, lane_ing, 'trajectory')  # get coordinates of trajectory
            
            lane_objects[traj_id] = Lane(traj_id, traj_coordinates,'trajectory')  # define Lane object and add it to lane_objects

        else:  # egress
            lane_objects[id] = Lane(id, coordinaten, 'egress', signal)
    return lane_objects
            

def get_signal_objects(dict_signals) -> dict:
    #print(dict_signals)
    'Get a list of all the Signals'
    signals ={} 
    for _ , j in dict_signals.items():
        if j['traffic_light'] != '':
            signals[j['traffic_light']] = Signal(j['traffic_light'])
    return signals

def get_inductioncoils(sensors_all_lanes, lane_objects) -> dict:
    ' define a list of InductionCoils objects'
    
    inductioncoils = {}# list of all the inductioncoils of all the lanes

    for lane in lane_objects.values(): # iterate through each lane
        if lane.getTypeLane() != 'trajectory':
            id = lane.getID()
            if bool(sensors_all_lanes[id]['sensors']): # check if lane contains inductionscoils

                # iterate through inductionloops
                for sensorID in sensors_all_lanes[id]['sensors'].keys():
                    centerposition = sensors_all_lanes[id]['sensors'][sensorID]['position'] # get the centerlocation/ Sensorposition
                    sensor_length = sensors_all_lanes[id]['sensors'][sensorID]['length'] # get the length 
                    
                    #Define InductionCoil
                    centerposition = tuple(map(lambda x: int(x) /10000000, centerposition))
                    distance = lane.coordinate_to_meters(centerposition)
                    centerlocation = Location(lane, distance)
                    induction_coil = InductionCoil(sensorID, centerlocation, float(sensor_length)/100)

                    # Add to list inductioncoils
                    inductioncoils[sensorID] = induction_coil
                    # set induction_coil to lane
                    # lane_objects[id].setInductionloop(induction_coil) #TODO add induction coils properly

    return inductioncoils


def load_lanes_signals_and_inductioncoils() -> (dict, dict, dict):
    layout_paths = get_available_intersections()    # example: ['BOS210', 'BOS211']

    lanes = {}
    signals = {}
    inductioncoils = {}
    for filename in layout_paths:

        root = open_xml(filename)
        # Define the necessary dictionaries that will be used to define our class objects
        vehicles_lanes = vehicles_laneID(root)   # Get the laneID en genericlane of all lane that is specific for vehicles
        lane_indcoil_signal = get_dict_lane_info(filename)  # dictionary of the induction loops and trafficlights of  all lanes
        lanes_length = get_length_all_lanes(filename)  # dictionary of the length of all lanes
        sensors_all_lanes = get_dict_sensor_info(filename)
        #return lane objects, signals inductioncoils

        # Define the Lane objects
        lanes = get_lane_objects(vehicles_lanes, lane_indcoil_signal, root)

        #Define the Signal objects
        signals = get_signal_objects(lane_indcoil_signal)

        #Define the InductionCoil objects
        inductioncoils = get_inductioncoils(sensors_all_lanes, lanes)
    
        lanes.update(lanes)
        signals.update(signals)
        inductioncoils.update(inductioncoils)
    return (lanes, signals, inductioncoils)



    # define een World


    # define een World


    # define een World


    # define een World


    # define een World


    # define een World


    # define een World


    # define een World


    # define een World


    # define een World


    # define een World


    # define een World


    # define een World
    # kruispunt = World(1, cars, lane_objects.values(), n_signals, n_inductioncoils, 100.0)
    # for car in cars:
    #     savefile = 'testCar' + car.location.lane.id  # TODO add world time
    #     with open(os.path.join('cars_movements', savefile), 'w') as csvfile:
    #         fieldnames = ['time', 'latitude', 'longitude']
    #         writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=fieldnames)
    #         writer.writeheader()

    #         test_lane = lane_objects.get('1')
    #         test_car = cars[0]

    #         t = 1604271611700
    #         step_size = 100  # miliseconds

    #         while 0 < car.location.meters_from_intersection < car.location.lane.length:
    #             car_geo = car.location.to_geo()
    #             writer.writerow({'time': t, 'latitude': car_geo[0], 'longitude': car_geo[1]})
    #             car.move(step_size)
    #             t += step_size
