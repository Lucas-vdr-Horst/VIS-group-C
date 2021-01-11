import os
from const import intersection_data_location
from common import get_csv_paths, get_available_intersections, get_header
from alive_progress import alive_bar
from datetime import datetime


def datetime_string_to_milli(datetime_string) -> int:
    """Datetime in string format '%d-%m-%Y %H:%M:%S.%f' to milliseconds since 1970"""
    datetime_obj = datetime.strptime(datetime_string, '%d-%m-%Y %H:%M:%S.%f')
    return int(int(datetime_obj.strftime('%s')) * 1000 + int(datetime_obj.strftime('%f')) / 1000)


def compress_csvs() -> None:
    for intersection in get_available_intersections():
        compressed_directory = os.path.join(intersection_data_location, intersection, 'compressed')
        if not os.path.exists(compressed_directory):
            os.makedirs(compressed_directory)
        compressed_file_path = os.path.join(compressed_directory, 'compressed.csv')
        if os.path.exists(compressed_file_path):
            os.remove(compressed_file_path)

        with open(compressed_file_path, 'a') as compressed_file:
            compressed_file.write(f"start_time;end_time{get_header(get_csv_paths(intersection)[0])[4:]}\n")

            working_state = None
            first_time = None
            last_time = None
            for uncompressed in get_csv_paths(intersection):
                with alive_bar(len(open(uncompressed).readlines()), title=uncompressed) as bar:
                    for i, line in enumerate(open(uncompressed)):
                        if i == 1:
                            working_state = line[22:]
                            first_time = datetime_string_to_milli(line[:21])
                            last_time = first_time
                        elif i > 0:
                            state = line[22:]
                            time = datetime_string_to_milli(line[:21])
                            if working_state != state:
                                compressed_file.write(f"{first_time};{last_time};{working_state}")
                                working_state = state
                                first_time = time
                            last_time = time

                        bar()
                    compressed_file.write(f"{first_time};{last_time};{working_state}")


if __name__ == '__main__':
    compress_csvs()
