from unittest import TestCase
import os
import pandas as pd

import sys

from preprocess.process_spawnpoints import process_certain_positions

from simulation.run_simulation import load_lanes_signals_and_inductioncoils


class Test(TestCase):

    def test_process_certain_positions(self):
        dict_induction_coils = load_lanes_signals_and_inductioncoils()
        process_certain_positions(dict_induction_coils)

        path = os.path.join("tests", "filetest", "test_spawn_points.csv")
        expected_output = pd.read_csv(path, sep=';', nrows=9)

        path2 = os.path.join("preprocess", "output", "spawn_points.csv")
        output_file = pd.read_csv(path2, sep=';', nrows=9)

        output = pd.DataFrame.equals(output_file, expected_output)

        self.assertEqual(output, True)
