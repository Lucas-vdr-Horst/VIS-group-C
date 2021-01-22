import os
from unittest import TestCase

import numpy as np
import pandas as pd


from preprocess.preprocess_extern_data import convert_to_coordinates, convert_to_float, add_sec, insert_row


class Test(TestCase):
    def test_convert_to_coordinates(self):
        coordinate ='51.673.774.6'

        output = convert_to_coordinates(coordinate)
        expected_output = 51.6737746

        self.assertEqual(output, expected_output)


    def test_convert_to_float(self):
        item = '52,1'

        output = convert_to_float(item)
        expected_output = 52.1

        self.assertEqual(output, expected_output)


    def test_add_sec(self):
        item = "12-1-2021 14:59"
        starter_sec = [24]

        output = add_sec(item, starter_sec)
        expected_output = 1610459964000

        self.assertEqual(output, expected_output)


    def test_insert_row(self):
        # This file test is good. But because 1 dataframe has float nans and 1 dataframe has np.nans and i couldnt fix it that it was equal to each other
        path = os.path.join("intersections", "BOS210", "BOS210.csv")
        df = pd.read_csv(path, sep=";", dtype=str)
        output = insert_row(df, 1, df.loc[1])
        output_sample = pd.DataFrame(output.iloc[0:5,0:5])

        data = {'time':['02-11-2020 00:00:00.0', '02-11-2020 00:00:00.1', '02-11-2020 00:00:00.1', '02-11-2020 00:00:00.2', '02-11-2020 00:00:00.3'], '01':[np.nan, np.nan, np.nan, np.nan, np.nan], '03':[np.nan, np.nan, np.nan, np.nan, np.nan], '04':[np.nan, np.nan, np.nan, np.nan, np.nan], '05':[np.nan, np.nan, np.nan, np.nan, np.nan]}

        expected_output = pd.DataFrame(data)

        df_equal = pd.DataFrame.equals(output_sample, expected_output)
        self.assertEqual(True, df_equal)