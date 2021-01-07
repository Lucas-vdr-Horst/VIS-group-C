from flask import Flask, request, send_from_directory, send_file
import glob
import json
from processing_module import process
import os
from datetime import datetime
from common import read_csvs


app = Flask(__name__)
intersection_data_location = os.path.join('intersections', '')


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
def get_available_intersections():
    return json.dumps([i.replace(intersection_data_location, '') for i in glob.glob(os.path.join(intersection_data_location, '*'))])


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
    csvs = read_csvs(intersection_name)
    return send_file(csvs[index])


@app.route('/amount_sensor_data/<intersection_name>')
def get_amount_csv(intersection_name):
    return str(len(read_csvs(intersection_name)))


@app.route('/available_times/<intersection_name>')
def get_available_times(intersection_name):
    csvs = read_csvs(intersection_name)
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
    # TODO
    timeframe = json.loads(timeframe_string)  # example: {'begin': 1604272907812, 'end': 1604273470312}
    return json.dumps({1604272907812: {'05': 1, '06': 0}, 1604272907813: {'05': 0, '06': 1}})


@app.route('/car_request')
def car_request():
    begin_time = request.values.get('begin_time')
    end_time = request.values.get('begin_time')
    return process(begin_time, end_time)


if __name__ == "__main__":
    app.run(host='localhost', debug=True)
