from flask import Flask, request, send_from_directory, send_file
import glob
import json
from processing_module import process
import os

app = Flask(__name__)
layouts_location = os.path.join('dataset', 'layouts')


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/layout/<path:path>')
def send_layout(path):
    return send_from_directory(layouts_location, path)


@app.route('/')
def homepage():
    return send_file('static/home.html')


@app.route('/car_request')
def car_request():
    begin_time = request.value.get('begin_time')
    end_time = request.values.get('begin_time')
    return process(begin_time, end_time)


@app.route('/available_layouts')
def get_available_layouts():
    return json.dumps([i.replace(layouts_location, '') for i in glob.glob(os.path.join(layouts_location, '*.xml'))])


if __name__ == "__main__":
    app.run(host='localhost', debug=True)
