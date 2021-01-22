import os
from unittest import TestCase

import sys
import pandas as pd


from preprocess.preprocess_extern_data import convert_to_coordinates, convert_to_float, add_sec, insert_row


class Test(TestCase):
    def test_convert_to_coordinates(self):
        coordinate ='51.673.77.4.6'

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
        starter_sec = 24

        output = add_sec(item, starter_sec)
        expected_output = 1610459964000

        self.assertEqual(output, expected_output)


    def test_insert_row(self):
        path = os.path.join("intersections", "BOS210", "BOS210.csv")
        df = pd.read_csv(path, sep=";")
        output = insert_row(df, 556, df.loc[556])
        print(output)
        expected_output = '2'
        self.assertEqual(output, expected_output)


    def test_read_extern_data(self):
        self.assertEqual(1,2)




