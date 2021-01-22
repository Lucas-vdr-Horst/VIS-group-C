from const import cars_data_location
import os
import glob
from alive_progress import alive_bar

timeframes = []


def load_car_timeframes() -> None:
    csv_paths = glob.glob(os.path.join(cars_data_location, '*csv'))
    with alive_bar(len(csv_paths), title='Loading car timeframes') as bar:
        for csv_path in csv_paths:
            lines = open(csv_path).read().split('\n')
            lines = tuple(filter(lambda x: x != '', lines))
            timeframes.append({
                'name': csv_path.replace(cars_data_location, '').replace('.csv', ''),
                'begin': int(lines[1].split(';')[0]),
                'end': int(lines[-1].split(';')[0])
            })
            bar()


def get_cars_around_block(block: int, block_size: int) -> list:
    return [t['name'] for t in timeframes if t['begin']-block_size <= block*block_size <= t['end']]


def first_time() -> int:
    return min([f['begin'] for f in timeframes])


load_car_timeframes()
