import os
from const import intersection_data_location
from common import get_csv_paths, get_available_intersections, get_header, timeframe_csv, datetime_string_to_milli
from alive_progress import alive_bar


def compress_csvs() -> None:
    """
    Get a compressed csv with information about the traffic lights and inductionloops.

    @returns: a csv file compressed
    """
    for intersection in get_available_intersections():
        compressed_directory = os.path.join(intersection_data_location, intersection, 'compressed')
        if not os.path.exists(compressed_directory):
            os.makedirs(compressed_directory)
        compressed_file_path = os.path.join(compressed_directory, 'compressed.csv')
        if os.path.exists(compressed_file_path):
            os.remove(compressed_file_path)

        with open(compressed_file_path, 'a') as compressed_file:
            compressed_file.write(f"start_time;end_time{get_header(get_csv_paths(intersection)[0])[4:]}\n")
            csv_paths = get_csv_paths(intersection)
            csv_paths.sort(key=lambda x: datetime_string_to_milli(timeframe_csv(x)[0]))

            working_state = None
            first_time = None
            for uncompressed in csv_paths:
                with alive_bar(len(open(uncompressed).readlines()), title=uncompressed) as bar:
                    for i, line in enumerate(open(uncompressed)):
                        if i == 1:
                            working_state = line[22:]
                            first_time = datetime_string_to_milli(line[:21])
                        elif i > 0:
                            state = line[22:]
                            time = datetime_string_to_milli(line[:21])
                            if working_state != state:
                                compressed_file.write(f"{first_time};{time-1};{working_state}")
                                working_state = state
                                first_time = time

                        bar()
                    compressed_file.write(f"{first_time};{time-1};{working_state}")