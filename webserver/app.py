from flask import Flask, request, send_from_directory, send_file
import glob
import json
import os
import sys

sys.path.append('../')
import common
from const import *
from .binary_search_load import get_inputs_block
from .car_timeframe_load import get_cars_around_block, first_time

parent_path = os.path.join(os.path.dirname(__file__), '..')
app = Flask(__name__)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/')
def homepage():
    return send_file('static/home.html')


@app.route('/favicon.ico')
def favicon():
    return send_file('static/favicon.ico')


@app.route('/available_intersections')
def available_intersections():
    return json.dumps(common.get_available_intersections())


@app.route('/layout/<intersection_name>')
def send_layout(intersection_name):
    path = os.path.join(parent_path, intersection_data_location, intersection_name, '*.xml')
    layouts = glob.glob(path)
    if len(layouts) == 1:
        return send_file(layouts[0])
    else:
        print(path)
        return 'No or multiple .xml files', 404


@app.route('/available_times/<intersection_name>')
def get_available_times(intersection_name):
    csvs = common.get_csv_paths(intersection_name)
    lst = []
    for csv in csvs:
        with open(csv) as file:
            lines = file.readlines()
            start_time = lines[1][0:21]
            start_time = common.to_datetime(start_time)
            end_time = lines[-2][0:21]
            end_time = common.to_datetime(end_time)
            lst.append([start_time, end_time])

    return json.dumps(lst, default=str)


@app.route('/header_names')
def get_header_names():
    intersection_headers = {}
    for intersection in common.get_available_intersections():
        csv_filename = common.get_csv_paths(intersection)[0]
        intersection_headers[intersection] = common.read_lines(csv_filename, [0])[0].replace('time;', '').split(';')
    return intersection_headers


@app.route('/sensor_blocks')
def get_sensor_blocks():
    intersection, time = request.values.get('intersection'), int(request.values.get('time'))
    block, found = get_inputs_block(time, intersection)
    if found:
        blocks = [{'begin': block['begin'], 'end': block['end'], 'state': block['state']}]
        lines = open(
            os.path.join(parent_path, intersection_data_location, intersection, 'compressed', 'compressed.csv')).read().split('\n')
        for i in range(block['index'] + 1, min(block['index'] + 10, len(lines) - 1)):
            split = lines[i].split(';')
            blocks.append({
                'begin': int(split[0]),
                'end': int(split[1]),
                'state': ';'.join(split[2:])
            })
        return json.dumps(blocks)
    else:
        return 'Time-block not found'


@app.route('/cars_around_block/<int:block>')
def cars_around_time(block):
    return json.dumps(get_cars_around_block(block, cars_block_size))


@app.route('/car/<path:path>')
def send_car(path):
    return send_from_directory(os.path.join(parent_path, cars_data_location), path+'.csv')


@app.route('/interesting_time')
def get_interesting_time():
    return str(first_time()+100)
