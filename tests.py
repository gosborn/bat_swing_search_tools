import unittest

from bat_swing_search import (
    search_continuity_above_value,
    back_search_continuity_within_range,
    search_continuity_above_value_two_signals,
    search_multi_continuity_within_range,
    map_data_to_index,
    validate_params,
)


SWING_FIXTURE = [
    ['0', -1.163086, 0.238281, -1.051758, 4.81493, -15.695393, -6.593897],
    ['1249', -1.136719, 0.265625, 3.0, 4.736102, -15.614434, -6.480981],
    ['2497', -1.118164, 0.285156, 3.0, 4.659403, -15.50791, -6.359542],
    ['3746', -1.087891, 0.293945, 3.0, 4.667925, -15.38221, -6.250887],
    ['4996', -0.972656, 0.323242, 3.0, 4.72758, -15.226684, -6.165667],
    ['6243', -0.904297, 0.388672, 2.9, 4.725449, -15.032808, -6.078316],
    ['7492', -0.869141, 0.456055, 3.0, 4.638098, -14.843193, -5.96327],
    ['8741', -0.874023, 0.49707, 3.0, 4.544357, -14.69832, -5.782177],
    ['9989', -0.898438, 0.543945, 3.0, 4.486833, -14.574751, -5.5393],
    ['11238', -0.869141, 0.558594, 3.0, 4.478311, -14.474617, -5.28364],
]


class SearchContinuityAboveValueTestCase(unittest.TestCase):

    def test_value_exists(self):
        index = search_continuity_above_value('ax', 0, 9, -2, 4, SWING_FIXTURE)
        self.assertEqual(index, 0)

    def test_value_does_not_exist(self):
        result = search_continuity_above_value('ax', 0, 9, 1, 5, SWING_FIXTURE)
        self.assertEqual(result, None)


class BackSearchContinuityWithinRange(unittest.TestCase):

    def test_value_exists(self):
        index = back_search_continuity_within_range('ax', 9, 0, -2, -0.9, 4, SWING_FIXTURE)
        self.assertEqual(index, 5)

    def test_value_does_not_exist(self):
        result = back_search_continuity_within_range('ax', 9, 0, 1, 3, 4, SWING_FIXTURE)
        self.assertEqual(result, None)


class SearchContinuityAboveTwoSignals(unittest.TestCase):

    def test_value_exists(self):
        index = search_continuity_above_value_two_signals('ax', 'ay', 0, 9, -1, 0.3, 3, SWING_FIXTURE)
        self.assertEqual(index, 4)

    def test_value_does_not_exist(self):
        result = search_continuity_above_value_two_signals('ax', 'ay', 0, 9, 1, 0.3, 3, SWING_FIXTURE)
        self.assertEqual(result, None)


class SearchMultiContinuityWithinRange(unittest.TestCase):

    def test_value_exists(self):
        result = search_multi_continuity_within_range('az', 0, 9, 2.9, 3.1, 3, SWING_FIXTURE)
        self.assertEqual(result, [[1, 3], [2, 4], [6, 8], [7, 9]])

    def test_value_does_not_exist(self):
        result = search_multi_continuity_within_range('ax', 0, 9, 2, 5, 3, SWING_FIXTURE)
        self.assertEqual(result, [])


class UtilityTests(unittest.TestCase):

    def test_map_data_to_index(self):
        data = 'foo'
        with self.assertRaises(Exception):
            map_data_to_index(data)

    def test_validate_params_index_begin(self):
        params = {
            'index_begin': -1
        }
        with self.assertRaises(Exception):
            validate_params(params)

    def test_validate_params_index_end(self):
        params = {
            'index_end': -1
        }
        with self.assertRaises(Exception):
            validate_params(params)

    def test_validate_params_threshold(self):
        params = {
            'index_end': 'foo'
        }
        with self.assertRaises(Exception):
            validate_params(params)

    def test_validate_params_win_length(self):
        params = {
            'win_length': 0
        }
        with self.assertRaises(Exception):
            validate_params(params)

    def test_validate_params_threshold_low(self):
        params = {
            'threshold_low': 'foo'
        }
        with self.assertRaises(Exception):
            validate_params(params)

    def test_validate_params_threshold_high(self):
        params = {
            'threshold_high': 'foo'
        }
        with self.assertRaises(Exception):
            validate_params(params)

    def test_validate_params_threshold_1(self):
        params = {
            'threshold_1': 'foo'
        }
        with self.assertRaises(Exception):
            validate_params(params)

    def test_validate_params_threshold_2(self):
        params = {
            'threshold_2': 'foo'
        }
        with self.assertRaises(Exception):
            validate_params(params)


if __name__ == '__main__':
    unittest.main()
