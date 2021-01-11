from flask import Flask, request, send_from_directory, send_file
import glob
import json
from processing_module import process
import os
from datetime import datetime
from common import get_csv_paths, read_lines, timeframe_csv, get_available_intersections
from const import intersection_data_location


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


@app.route('/sensor_data/<intersection_name>')
@app.route('/sensor_data/<intersection_name>/<index>')
def get_sensor_data(intersection_name, index=0):
    csvs = get_csv_paths(intersection_name)
    return send_file(csvs[index])


@app.route('/amount_sensor_data/<intersection_name>')
def get_amount_csv(intersection_name):
    return str(len(get_csv_paths(intersection_name)))


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


@app.route('/sensor_timeframe/<timeframe_string>')
def sensor_timeframe(timeframe_string):
    timeframe = json.loads(timeframe_string)  # example: {'begin': 1604272907812, 'end': 1604273470312}
    sp = json.load(open(os.path.join('preprocessed', 'sensors_preprocessed.json')))

    begin_index, end_index = 0, -1
    if int(timeframe['begin']) > int(tuple(sp.keys())[begin_index]):
        begin_index = list(sp.keys()).index(timeframe['begin'])
    if int(timeframe['end']) > int(tuple(sp.keys())[end_index]):
        end_index = list(sp.keys()).index(timeframe['end'])

    result = {time: states for time, states in list(sp.items())[begin_index:end_index+1]}

    return json.dumps(result)


@app.route('/header_names')
def get_header_names():
    intersection_headers = {}
    for intersection in json.loads(get_available_intersections()):
        csv_filename = get_csv_paths(intersection)[0]
        intersection_headers[intersection] = read_lines(csv_filename, [0])[0].replace('time;', '').split(';')
    return intersection_headers


def read_block(filename: str, start_index: int, block_size: int):
    result = []
    for i, line in enumerate(open(filename)):
        if i > start_index+block_size:
            break
        elif i > start_index:
            result.append(line[21:-1])
    return result


@app.route('/sensor_block/<int:time>')
def get_sensor_block(time):
    intersection_block = {}
    for intersection in json.loads(get_available_intersections()):
        for csv_filename in get_csv_paths(intersection):
            first_datetime, csv_length = timeframe_csv(csv_filename)
            first_mili = int(first_datetime.strftime('%s')) * 1000
            if first_mili < time < first_mili + csv_length*100:
                start_index = (time - first_mili) / 100
                intersection_block[intersection] = read_block(csv_filename, int(start_index), 5)
    return json.dumps(intersection_block)


@app.route('/car_request')
def car_request():
    begin_time = request.values.get('begin_time')
    end_time = request.values.get('begin_time')
    return process(begin_time, end_time)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
