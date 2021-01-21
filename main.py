from consolemenu import *
from consolemenu.items import *
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-O", "--option", help="Select a menu option")
parser.add_argument("-b", "--begin", help="Begin time in milliseconds")
parser.add_argument("-e", "--end", help="End time in milliseconds")
parser.add_argument("-pA", "--preprocess_all", help="Preprocess everything")
parser.add_argument("-pC", "--preprocess_compressed", help="Preprocess compressed.csv")
parser.add_argument("-pE", "--preprocess_externData", help="Preprocess the extern data")
parser.add_argument("-pS", "--preprocess_spawnpoints", help="Preprocess the spawnpoints")
parser.add_argument("-wL", "--webserver_local", help="Starts the webserver local")
parser.add_argument("-wO", "--webserver_open", help="Starts the open webserver")
parser.add_argument("-u", "--unit_test", help="Starts the unit test")


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
    args = parser.parse_args()
    if args.option is not None:
        if args.option == 'preprocessAll':
            all_preprocess()
        elif args.option == 'preprocessCompressed':
            compress_csvs()
        elif args.option == 'preprocessExternData':
            process_extern_data()
        elif args.option == 'preprocessSpawnpoints':
            process_spawnpoints()
        elif args.option == 'run_simulation':
            from simulation.run_simulation import run_simulation
            run_simulation(args.begin, args.end)
        elif args.option == 'webserver_local':
            webserver_local()
        elif args.option == 'webserver_open':
            webserver_open()
        elif args.option == 'unit_test':
            start_test()
    else:
        menu.show()
        #from simulation.run_simulation import run_simulation
        #run_simulation(1610189996000, 1610190056000)
        #webserver_local()
