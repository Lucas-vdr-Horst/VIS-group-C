import sys
import os
from unittest import TestCase

import pandas as pd
sys.path.append('./')
from preprocess.compress_csvs import compress_csvs


class Test(TestCase):

    def test_extract_info_csv(self):
        compress_csvs()
        test_csv_path = os.path.join("tests", "filetest", "test_compressed.csv")

        expected_output = pd.read_csv(test_csv_path, sep=';', nrows=9)

        test_csv_path = os.path.join("intersections", "BOS210", "compressed", "compressed.csv")

        output_file = pd.read_csv(test_csv_path, sep=';', nrows=9)

        output = pd.DataFrame.equals(output_file, expected_output)
        self.assertEqual(True, output)
