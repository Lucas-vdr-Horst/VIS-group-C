from common import get_available_intersections
from const import intersection_data_location
import os
import math
from alive_progress import alive_bar

inputs_blocks = {}  # key=intersection


def load_inputs_blocks():
    for intersection in get_available_intersections():
        inputs_blocks[intersection] = []
        filepath = os.path.join(intersection_data_location, intersection, 'compressed', 'compressed.csv')
        lines = tuple(filter(lambda l: len(l.split(';')) > 1, open(filepath).read().split('\n')[1:]))
        with alive_bar(len(lines), title=intersection) as bar:
            for i, line in enumerate(lines):
                split = line.split(';')
                inputs_blocks[intersection].append({
                    'begin': int(split[0]),
                    'end': int(split[1]),
                    'state': ';'.join(split[2:]),
                    'index': i+1
                })
                bar()


def binary_search_blocks(time: int, blocks: list) -> (dict, bool):
    if len(blocks) == 0:
        return {}, False
    center_index = math.floor(len(blocks) / 2)
    center_block = blocks[center_index]
    if center_block['begin'] <= time <= center_block['end']:
        return center_block, True
    if len(blocks) == 1:
        return {}, False

    if time < center_block['begin']:
        return binary_search_blocks(time, blocks[:center_index])
    else:
        return binary_search_blocks(time, blocks[center_index+1:])


def get_inputs_block(time: int, intersection: str) -> dict:
    return binary_search_blocks(time, inputs_blocks[intersection])


load_inputs_blocks()
