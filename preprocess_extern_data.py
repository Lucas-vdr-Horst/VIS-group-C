import os
import glob
import pandas as pd


def read_csv():
    intersection_data_location = os.path.join('extern_data', '')
    return glob.glob(os.path.join(intersection_data_location, '*.csv'))


def convert_to_int(item):
    item = int(item.replace('.', ''))
    item /= 1000000
    return item


def convert_to_float(item):
    item = float(item.replace(',', '.'))
    return item


def read_externe_data():
    df = pd.read_csv('extern_data\\rondjes_den_bos.csv', sep=';')
    print(df['Longitude'].head())
    df['Longitude'] = df['Longitude'].apply(convert_to_int)
    df['Latitude'] = df['Latitude'].apply(convert_to_int)
    df['Speed (km/h)'] = df['Speed (km/h)'].apply(convert_to_float)
    print(df.dtypes)
    print(df['Longitude'].head())
    print(df.head())
    df.to_csv("extern_data.csv", index=False)


if __name__ == "__main__":
    read_externe_data()


# preprocess tot dit
example = {"1604275200000": {'lat': 52.000, 'lon': 5.00}}