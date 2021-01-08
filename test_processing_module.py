from unittest import TestCase
from processing_module import calculate_markers_points


class Test(TestCase):
    def test_calculate_markers_points(self):
        lane13 = [51.6828358, 5.2942547]
        lane19 = [51.6829984, 5.2943788]
        print(type(lane19[0]))
        calulated_path = calculate_markers_points(lat1=lane13[0], lon1=lane13[1], lat2=lane19[0], lon2=lane19[1], marker_count=5)
        self.assertEqual(len(calulated_path), 5)
