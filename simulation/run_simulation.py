from simulation.classes.Lane import Lane
from simulation.classes.World import World
from simulation.classes.Car import Car
from simulation.classes.Signal import Signal
from simulation.classes.InductionCoil import InductionCoil
from simulation.classes.Location import Location
from simulation.classes.SignalManager import SignalManager

from preprocess.processing_module import get_coordinates, calculate_trajectory, get_lane, vehicles_laneID
from preprocess.lane_technical_information import get_dict_lane_info
from preprocess.sensor_technical_information import get_dict_sensor_info
from simulation.length_per_laneID import get_length_all_lanes
from common import open_xml, get_available_intersections, clear_cars_movements
from const import cars_data_location, intersection_data_location, car_length
import os
import csv
import glob
import names
from alive_progress import alive_bar


def run_simulation(begin_time: int, end_time: int) -> None:
    clear_cars_movements()

    lanes, signals, inductioncoils = load_lanes_signals_and_inductioncoils()
    worlds_array = []
    worlds_dict = {}
    car_merges = {}
    to_update = []

    def add_world(addworld: World, index=None) -> World:
        """
        Adds the world to the worlds_array and worlds_dict,
        if there is already world at that runtime, it merges them
        """
        if addworld.runtime in worlds_dict:
            existing_world: World = worlds_dict[addworld.runtime]
            existing_world.merge_world_into(addworld, car_merges)
            return existing_world
        else:
            worlds_array.insert(index if index is not None else len(worlds_array), addworld)
            worlds_dict[addworld.runtime] = addworld
            return addworld

    # Initialize worlds with car spawn points
    with open(os.path.join('preprocess', 'output', 'spawn_points.csv')) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        next(reader, None)
        for i, row in enumerate(reader):
            time = int(row[0])
            if time >= begin_time:
                if time <= end_time:
                    car = Car(str(i), Location(lanes[row[1]], float(row[2])), car_length, 8.3)
                    car_merges[car.id] = car.id
                    world = World([car], lanes, signals, inductioncoils, time)
                    add_world(world)
                else:
                    break
    print('Loaded spawn points, now simulating')

    # Main simulation loop
    to_update.append(worlds_array[0])
    while to_update:
        update_world = to_update.pop(0)
        print(f"{begin_time} - {update_world.runtime} - {end_time}", end='\r')
        next_world = update_world.next_world(100)
        next_world = add_world(next_world, worlds_array.index(update_world) + 1)
        if begin_time < next_world.runtime < end_time:
            to_update.append(next_world)
    print('Simulation done, now exporting')

    # Export to csv's

    # Don't know why this happens but this should fix it
    for fix_key, fix_value in [(k, car_merges[v]) for k, v in car_merges.items() if car_merges[v] != v]:
        car_merges[fix_key] = fix_value
    unique_cars = tuple(set(car_merges.values()))
    export_paths = {i: os.path.join(cars_data_location, f'sim_car_{i}.csv') for i in unique_cars}
    for filepath in export_paths.values():
        with open(filepath, 'w') as file:
            writer = csv.writer(file, delimiter=';', lineterminator='\n')
            writer.writerow(('time', 'latitude', 'longitude'))
    for world in worlds_array:
        print(f"{world.runtime} / {worlds_array[-1].runtime}", end='\r')
        for car in world.cars.values():
            with open(export_paths[car_merges[car.id]], 'a') as file:
                file.write(';'.join(map(str, (world.runtime, *car.location.to_geo())))+'\n')
    print('Exported, done!')


def get_lane_objects(vehicles_lanes, lane_indcoil_signal, root, filename) -> dict:
    """
    Return a list containing defined Lane objects of all the vehicle lanes in specified filename

    For our simulation, we will be focusing on the lane that is intended for a vehicle.
    """
    lane_objects = {}  # dict containing the Lane Objects

    for id in vehicles_lanes.keys():  # iterate through each  lane

        # Defining Signal object of  lane
        if id.zfill(2) in lane_indcoil_signal.keys() and lane_indcoil_signal[id.zfill(2)][
            'traffic_light'] != '':  # check if laneID of  lane in dict and if  lane contains any traffic lights
            signal_id = lane_indcoil_signal[id.zfill(2)]['traffic_light']  # get the signal_id

            signal = Signal(signal_id)  # define Signal object
        else:
            signal = None

        coordinaten = get_coordinates(root, vehicles_lanes[id], 'ingress')  # [::-1] # get the coordinates of  lane

        # Define Lane object based on the type of the lane.
        # An ingresslane contains the necessary coordinates of an trajectory. 
        # We can directly define an trajectory Lane object and an ingress Lane object. 
        if vehicles_lanes[id][3][0].text == '10':  # ingress
            linked_egresslane = vehicles_lanes[id][5][0][0][0].text
            laneid = filename + "_" + id
            # laneid = id
            lane_objects[laneid] = Lane(laneid, coordinaten[::-1], 'ingress', signal)  # add to dict

            # Define the instance variable for a Lane object of a trajectory
            lane_ing = get_lane(root, id)
            traj_id = filename + "_" + id + '-' + linked_egresslane  # define the id
            # traj_id = id + '-' + linked_egresslane  # define the id
            traj_coordinates = get_coordinates(root, lane_ing, 'trajectory')  # get coordinates of trajectory

            lane_objects[traj_id] = Lane(traj_id, traj_coordinates,
                                         'trajectory')  # define Lane object and add it to lane_objects

        else:  # egress
            laneid = filename + "_" + id
            # laneid = id
            lane_objects[laneid] = Lane(laneid, coordinaten, 'egress', signal)

  
    for lane in lane_objects:
        if "-" in lane:
            temp = lane.split('-')  # bos210_1-26 -> bos210_1, 26->bos210_26

            ingress_lane = lane_objects.get(temp[0])
            traject_lane = lane_objects.get(lane)
            egress_lane = lane_objects.get(filename + '_' + temp[1])

            ingress_lane.connectedlane(traject_lane)
            traject_lane.connectedlane(egress_lane)
    return lane_objects


def get_signal_objects(dict_signals) -> dict:
    # print(dict_signals)
    'Get a list of all the Signals'
    signals = {}
    for _, j in dict_signals.items():
        if j['traffic_light'] != '':
            signals[j['traffic_light']] = Signal(j['traffic_light'])
    return signals


def get_inductioncoils(sensors_all_lanes, lane_objects) -> dict:
    ' define a list of InductionCoils objects'

    inductioncoils = {}  # list of all the inductioncoils of all the lanes

    for lane in lane_objects.values():  # iterate through each lane
        if lane.getTypeLane() != 'trajectory':
            id = lane.getID().split('_')[1]  # bos210_1 -> get 1
            if bool(sensors_all_lanes[id]['sensors']):  # check if lane contains inductionscoils

                # iterate through inductionloops
                for sensorID in sensors_all_lanes[id]['sensors'].keys():
                    centerposition = sensors_all_lanes[id]['sensors'][sensorID][
                        'position']  # get the centerlocation/ Sensorposition
                    sensor_length = sensors_all_lanes[id]['sensors'][sensorID]['length']  # get the length

                    # Define InductionCoil
                    centerposition = tuple(map(lambda x: int(x) / 10000000, centerposition))
                    distance = lane.coordinate_to_meters(centerposition)
                    centerlocation = Location(lane, distance)
                    induction_coil = InductionCoil(sensorID, centerlocation, float(sensor_length) / 100)

                    # Add to list inductioncoils
                    inductioncoils[sensorID] = induction_coil
 

    return inductioncoils


def load_lanes_signals_and_inductioncoils() -> (dict, dict, dict):
    layout_paths = get_available_intersections()  # example: ['BOS210', 'BOS211']

    lanes = {}
    signals = {}
    inductioncoils = {}
    for filename in layout_paths:

        root = open_xml(filename)
        # Define the necessary dictionaries that will be used to define our class objects
        vehicles_lanes = vehicles_laneID(
            root)  # Get the laneID en genericlane of all lane that is specific for vehicles
        lane_indcoil_signal = get_dict_lane_info(
            filename)  # dictionary of the induction loops and trafficlights of  all lanes
        lanes_length = get_length_all_lanes(filename)  # dictionary of the length of all lanes
        sensors_all_lanes = get_dict_sensor_info(filename)
        # return lane objects, signals inductioncoils

        # Define the Lane objects
        lanes = get_lane_objects(vehicles_lanes, lane_indcoil_signal, root, filename)

        # Define the Signal objects
        signals = get_signal_objects(lane_indcoil_signal)
        for signal in signals:
            signals[signal].setIntersection(filename)
        # Define the InductionCoil objects
        inductioncoils = get_inductioncoils(sensors_all_lanes, lanes)
        for inductioncoil in inductioncoils:
            inductioncoils[inductioncoil].setIntersection(filename)

        lanes.update(lanes)
        signals.update(signals)
        inductioncoils.update(inductioncoils)

    pathlst = []
    for intersection in get_available_intersections():
        path = os.path.join(intersection_data_location, intersection, "compressed", "compressed.csv")
        pathlst.append(path)
    # print(pathlst)
    signalMg = SignalManager(pathlst)
    for signal in signals:
        signals.get(signal).setSignalManager(signalMg)  # Cant check if this works yet
        #print(signals.get(signal).getState(1610492290820))
        #print("the signal id's are: ",signals.get(signal).id)

    for inductioncoil in inductioncoils:
        inductioncoils.get(inductioncoil).setSignalManager(signalMg)  # Cant check if this works yet

    for lane in lanes:
        #print(lanes.get(lane).id)
        continue

    return (lanes, signals, inductioncoils)

