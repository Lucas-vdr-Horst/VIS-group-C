from consolemenu import *
from consolemenu.items import *


def preprocess():
    from preprocess.compress_csvs import compress_csvs
    compress_csvs()


def process_simulation():
    from simulation.run_simulation import run_simulation
    run_simulation()


def start_webserver():
    from webserver.app import app
    app.run(host='0.0.0.0')


menu = ConsoleMenu("Vialis Intersection Simulation", "Start Menu")

menu.append_item(FunctionItem("Preprocess", preprocess))
menu.append_item(FunctionItem("Process simulation", process_simulation))
menu.append_item(FunctionItem("Start webserver", start_webserver))

if __name__ == '__main__':
    menu.show()
