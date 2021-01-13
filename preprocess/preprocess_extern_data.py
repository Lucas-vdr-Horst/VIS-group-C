import os
import pandas as pd


def read_data(file):
    """
    Creates a path to the right file in a friendly way for both linux and windows.
    """
    intersection_data_location = os.path.join('..','extern_data', '')
    return os.path.join(intersection_data_location, f'{file}.csv')


def convert_to_coordinates(item):
    """
    If item is a string
        removes the multiple dots in the number to convert it to an int. Afterwords the numbers
        are divided by 1 million to transform the numbers into coordinates.
    """
    if isinstance(item, str):
        item = int(item.replace('.', ''))
        item /= 1000000
    return item


def convert_to_float(item):
    """
    If item is a string
        Replaces the ',' with a dot to convert it to a float
    """
    if isinstance(item, str):
        item = float(item.replace(',', '.'))
    return item


def read_externe_data(filename):
    """
    The data is loaded into a panda dataframe so all values can be converted to the right type
    afterwards the dataframe will be uploaded to an csv file. If the csv already existed it will
    be removed so it can be replaced by the new dataframe.
    """
    file = read_data(filename)
    try: # if the file doesn't have the right separator
        df = pd.read_csv(file, sep=';')
        print(df['Longitude'].head())
    except: # if the file has the right separator
        df = pd.read_csv(file)
    df['Longitude'] = df['Longitude'].apply(convert_to_coordinates)
    df['Latitude'] = df['Latitude'].apply(convert_to_coordinates)
    df['Speed (km/h)'] = df['Speed (km/h)'].apply(convert_to_float)
    if os.path.exists(file):  # deletes file to prevent duplicate if exist
        os.remove(file)
    df.to_csv(file, index=False)


if __name__ == "__main__":
    read_externe_data("extern_data")
