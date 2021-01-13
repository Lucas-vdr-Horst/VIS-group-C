from flask import Flask, request, send_from_directory, send_file
import glob
import json
from processing_module import process
import os
from datetime import datetime
from common import get_csv_paths, read_lines, timeframe_csv, get_available_intersections
from const import intersection_data_location
from binary_search_load import get_inputs_block


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
    return json.dumps(get_available_intersections())


@app.route('/layout/<intersection_name>')
def send_layout(intersection_name):
    layouts = glob.glob(os.path.join(intersection_data_location, intersection_name, '*.xml'))
    if len(layouts) == 1:
        return send_file(layouts[0])
    else:
        return 'No or multiple .xml files', 404


@app.route('/available_times/<intersection_name>')
def get_available_times(intersection_name):
    csvs = get_csv_paths(intersection_name)
    lst = []
    for csv in csvs:
        with open(csv) as file:
            lines = file.readlines()
            start_time = lines[1][0:21]
            start_time = datetime.strptime(start_time, '%d-%m-%Y %H:%M:%S.%f')
            end_time = lines[-2][0:21]
            end_time = datetime.strptime(end_time, '%d-%m-%Y %H:%M:%S.%f')
            lst.append([start_time, end_time])

    return json.dumps(lst, default=str)


@app.route('/header_names')
def get_header_names():
    intersection_headers = {}
    for intersection in get_available_intersections():
        csv_filename = get_csv_paths(intersection)[0]
        intersection_headers[intersection] = read_lines(csv_filename, [0])[0].replace('time;', '').split(';')
    return intersection_headers


@app.route('/sensor_blocks')
def get_sensor_blocks():
    intersection, time = request.values.get('intersection'), int(request.values.get('time'))
    block, found = get_inputs_block(time, intersection)
    if found:
        blocks = [{'begin': block['begin'], 'end': block['end'], 'state': block['state']}]
        lines = open(os.path.join(intersection_data_location, intersection, 'compressed', 'compressed.csv')).read().split('\n')
        for i in range(block['index']+1, min(block['index']+10, len(lines)-1)):
            split = lines[i].split(';')
            blocks.append({
                'begin': int(split[0]),
                'end': int(split[1]),
                'state': ';'.join(split[2:])
            })
        return json.dumps(blocks)
    else:
        return 'Time-block not found'


@app.route('/car_request')
def car_request():
    begin_time = request.values.get('begin_time')
    end_time = request.values.get('begin_time')
    return process(begin_time, end_time)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
