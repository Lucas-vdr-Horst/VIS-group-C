from consolemenu import *
from consolemenu.items import *


def preprocess():
    from preprocess.compress_csvs import compress_csvs
    from preprocess.preprocess_extern_data import read_extern_data
    read_extern_data()
    compress_csvs()


def process_simulation():
    from simulation.run_simulation import run_simulation
    print("What timeframe should be simulated?")
    begin_time = input('Begin datetime in milliseconds: ')
    end_time = input('End datetime in milliseconds: ')
    run_simulation(begin_time, end_time)


def webserver_local():
    from webserver.app import app
    app.run(host='localhost')


def webserver_open():
    from webserver.app import app
    app.run(host='0.0.0.0')


menu = ConsoleMenu("Start Menu")

menu.append_item(FunctionItem("Preprocess", preprocess))
menu.append_item(FunctionItem("Process simulation", process_simulation))

selection_webserver = ConsoleMenu('Webserver mode')
selection_webserver.append_item(FunctionItem("Local (only accessible for you)", webserver_local))
selection_webserver.append_item(FunctionItem("Open (accessible for everyone on the network)", webserver_open))
menu.append_item(SubmenuItem("Start Webserver", selection_webserver, menu))

if __name__ == '__main__':
    menu.show()
