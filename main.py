from consolemenu import *
from consolemenu.items import *
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-p", "--preprocess", help="Choose what to preprocess between: "
                                               "'compress', 'extern', 'spawnpoints' or 'all'")
parser.add_argument("-s", "--simulation", help="Give the begin and end time in milli second in format: begin-end")
parser.add_argument("-w", "--webserver", help="Choose the mode to start the webserver between: 'local' or 'open'")
parser.add_argument("-t", "--unittest", help="Choose a unit test between: ")#TODO


def compress_csvs():
    from preprocess.compress_csvs import compress_csvs
    compress_csvs()


def process_extern_data():
    from preprocess.preprocess_extern_data import read_extern_data
    read_extern_data()


def process_spawnpoints():
    from simulation.run_simulation import load_lanes_signals_and_inductioncoils
    from preprocess.process_spawnpoints import process_certain_positions
    lanes, signals, inductioncoils = load_lanes_signals_and_inductioncoils()
    process_certain_positions(inductioncoils)

def all_preprocess():
    compress_csvs()
    process_extern_data()
    process_spawnpoints()


def process_simulation():
    from simulation.run_simulation import run_simulation
    print("What timeframe should be simulated?")
    begin_time = int(input('Begin datetime in milliseconds: '))
    end_time = int(input('End datetime in milliseconds: '))
    run_simulation(begin_time, end_time)


def webserver_local():
    from webserver.app import app
    app.run(host='localhost')


def webserver_open():
    from webserver.app import app
    app.run(host='0.0.0.0')


def start_test():
    os.system('python -m unittest discover ./tests')


menu = ConsoleMenu("Start Menu")

selection_preprocess = ConsoleMenu('Preprocess')
selection_preprocess.append_item(FunctionItem("Compress csv", compress_csvs))
selection_preprocess.append_item(FunctionItem("Process extern data", process_extern_data))
selection_preprocess.append_item(FunctionItem("Process spawnpoints", process_spawnpoints))
selection_preprocess.append_item(FunctionItem("All of the above", all_preprocess))
menu.append_item(SubmenuItem("Preprocess", selection_preprocess, menu))

menu.append_item(FunctionItem("Process simulation", process_simulation))

selection_webserver = ConsoleMenu('Webserver mode')
selection_webserver.append_item(FunctionItem("Local (only accessible for you)", webserver_local))
selection_webserver.append_item(FunctionItem("Open (accessible for everyone on the network)", webserver_open))
menu.append_item(SubmenuItem("Start Webserver", selection_webserver, menu))
menu.append_item(FunctionItem("Unittest python function", start_test))

if __name__ == '__main__':
    open_menu = True
    args = parser.parse_args()
    if args.preprocess is not None:
        open_menu = False
        if args.preprocess == 'compress':
            compress_csvs()
        elif args.option == 'extern':
            process_extern_data()
        elif args.option == 'spawnpoints':
            process_spawnpoints()
        elif args.option == 'all':
            all_preprocess()
        else:
            raise Exception("For argument 'preprocess' choose between: 'compress', 'extern', 'spawnpoints' or 'all'")

    if args.simulation is not None:
        open_menu = False
        begin_time, end_time = map(int, args.simulation.split('-'))
        from simulation.run_simulation import run_simulation
        run_simulation(begin_time, end_time)

    if args.webserver is not None:
        open_menu = False
        if args.webserver == 'local':
            webserver_local()
        elif args.webserver == 'open':
            webserver_open()
        else:
            raise Exception("For argument 'webserver' choose between: 'local' or 'open'")

    if args.unittest is not None:
        open_menu = False
        start_test()

    if open_menu:
        menu.show()
