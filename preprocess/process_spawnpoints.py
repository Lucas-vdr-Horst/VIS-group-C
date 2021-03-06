import glob
import os
import csv
from alive_progress import alive_bar
from common import get_available_intersections
from const import intersection_data_location, car_length
from simulation.classes.InductionCoil import InductionCoil


def process_certain_positions(induction_coils: dict) -> None:
    """
    Uses the induction coil data from the `compressed.csv`'s to create a new `spawn_points.csv`.
    When a induction coil is activated or deactivate you know a car is at the beginning or end of the coil,
    these are the only positions of cars on times you know for certain so these are the "spawn points".
    A dictionary of induction-coils objects are needed to determen the location.
    """
    coils_dict = induction_coils

    csv_paths = [os.path.join(intersection_data_location, i, 'compressed', 'compressed.csv') for i in get_available_intersections()]
    last_state = {}  # key=coil_id, value=state
    n_lines = sum([len(open(p).readlines())-1 for p in csv_paths])

    with open(os.path.join('preprocess', 'output', 'spawn_points.csv'), 'w') as output_file:
        writer = csv.writer(output_file, delimiter=';', lineterminator='\n')
        writer.writerow(('time', 'lane_id', 'meters'))
        with alive_bar(n_lines, spinner='fishes') as bar:
            for filename in csv_paths[::-1]:
                with open(filename) as csv_file:
                    reader = csv.DictReader(csv_file, delimiter=';')
                    for row in reader:
                        row_start_time = int(row['start_time'])
                        for coil_id, value in row.items():
                            if coil_id in coils_dict:
                                if coil_id not in last_state:
                                    last_state[coil_id] = None
                                if last_state[coil_id] != value:
                                    coil_object: InductionCoil = coils_dict[coil_id]
                                    begin_pos, end_pos = coil_object.get_begin_and_end_locations()
                                    output_pos = begin_pos-car_length/2 if value == '|' else end_pos+car_length/2
                                    writer.writerow((row_start_time, output_pos.lane.id, output_pos.meters_from_intersection))

                                last_state[coil_id] = value
                        bar()
