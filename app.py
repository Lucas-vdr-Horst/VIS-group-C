from flask import Flask, request, send_from_directory, send_file
from processing_module import process

app = Flask(__name__)


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


@app.route('/layout/<path:path>')
def send_layout(path):
    return send_from_directory('dataset/layouts', path)


@app.route('/')
def homepage():
    return send_file('static/home.html')


@app.route('/car_request')
def car_request():
    begin_time = request.value.get('begin_time')
    end_time = request.values.get('begin_time')
    return process(begin_time, end_time)


if __name__ == "__main__":
    app.run(debug=True)
