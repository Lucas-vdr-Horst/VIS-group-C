import os
import pandas as pd


def read_csv_data(file):
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


def add_sec(item, i):
    if isinstance(item, str):
        item = f"{item}:{i[0] % 60}"
        i[0] += 1
    return item


def insert_row(dataframe, row, value):
    """
    https://www.geeksforgeeks.org/insert-row-at-given-position-in-pandas-dataframe/
    """
    df1 = dataframe[0:row]
    df2 = dataframe[row:]
    df1.loc[row] = value
    df = pd.concat([df1,df2])
    df.index = [*range(df.shape[0])]
    return df


def read_externe_data(filename):
    """
    The data is loaded into a panda dataframe so all values can be converted to the right type
    afterwards the dataframe will be uploaded to an csv file. If the csv already existed it will
    be removed so it can be replaced by the new dataframe.
    """
    file = read_csv_data(filename)
    new_filename = f'new_{filename}'
    new_file = read_csv_data(new_filename)
    try: # if the file doesn't have the right separator
        df = pd.read_csv(file, sep=';')
        print(df['Longitude'].head())
    except: # if the file has the right separator
        df = pd.read_csv(file)
    if filename == "extern_data":   # this is to fix only this file
        df = df.drop(752) # removing the 61 second of 15:11 minute
        df = insert_row(df, 556, df.loc[556])   # add a row with 0 speed to give that minute 60 sec in stead of 50
        df = insert_row(df, 1710, df.loc[1710]) # add a row with 0 speed to give that minute 60 sec in stead of 50
    first_min = df['time'].iloc[0]                          # to extract the amount of times the first min occurs, since
    sec_in_min_col = df['time'].value_counts().to_frame()   # the first min doesn't start at zero.
    value = [60 - sec_in_min_col.loc[first_min]['time']]    # The value is set in an list to create a correct variable for args
    df['time'] = df['time'].apply(add_sec, args=([value]))
    df['Longitude'] = df['Longitude'].apply(convert_to_coordinates)
    df['Latitude'] = df['Latitude'].apply(convert_to_coordinates)
    df['Speed (km/h)'] = df['Speed (km/h)'].apply(convert_to_float)
    if os.path.exists(new_file):  # deletes file to prevent duplicate if exist
        os.remove(new_file)
    df.to_csv(new_file, index=False)


if __name__ == "__main__":
    # test("extern_data")
    read_externe_data("extern_data")