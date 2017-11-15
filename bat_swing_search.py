import csv

INDEX_EXCEPTION_MESSAGE = 'index_begin or index_end does not exist in data set!'

swing_data = []

with open('latestSwing.csv', 'rb') as csv_file:
    reader = csv.reader(csv_file)
    for csv_row in reader:
        swing_data.append([csv_row[0], float(csv_row[1]), float(csv_row[2]), float(csv_row[3]),
                           float(csv_row[4]), float(csv_row[5]), float(csv_row[6])])


def search_continuity_above_value(data, index_begin, index_end, threshold, win_length, swing_to_analyze=None):
    validate_params(locals())
    data_index = map_data_to_index(data)
    swing_to_analyze = set_data(swing_to_analyze)

    start_index_of_continuity = index_begin
    current_index = index_begin
    data_points_above_threshold = 0

    try:
        while data_points_above_threshold < win_length and current_index <= index_end:
            if swing_to_analyze[current_index][data_index] > threshold:
                data_points_above_threshold += 1
            else:
                data_points_above_threshold = 0
                start_index_of_continuity = current_index + 1
            current_index += 1

        if data_points_above_threshold == win_length:
            return start_index_of_continuity
    except IndexError:
        raise Exception(INDEX_EXCEPTION_MESSAGE)


def back_search_continuity_within_range(data, index_begin, index_end, threshold_low,
                                        threshold_high, win_length, swing_to_analyze=None):
    validate_params(locals())
    data_index = map_data_to_index(data)
    swing_to_analyze = set_data(swing_to_analyze)

    start_index_of_continuity = index_begin
    current_index = index_begin
    data_points_within_range = 0

    try:
        while data_points_within_range < win_length and current_index >= index_end:
            if threshold_high > swing_to_analyze[current_index][data_index] > threshold_low:
                data_points_within_range += 1
            else:
                data_points_within_range = 0
                start_index_of_continuity = current_index - 1
            current_index -= 1

        if data_points_within_range == win_length:
            return start_index_of_continuity
    except IndexError:
        raise Exception(INDEX_EXCEPTION_MESSAGE)


def search_continuity_above_value_two_signals(data_1, data_2, index_begin, index_end, threshold_1,
                                              threshold_2, win_length, swing_to_analyze=None):
    validate_params(locals())
    swing_to_analyze = set_data(swing_to_analyze)
    data_index_1 = map_data_to_index(data_1)
    data_index_2 = map_data_to_index(data_2)

    start_index_of_continuity = index_begin
    current_index = index_begin
    data_points_above_both_thresholds = 0

    try:
        while data_points_above_both_thresholds < win_length and current_index <= index_end:
            row = swing_to_analyze[current_index]

            if row[data_index_1] > threshold_1 and row[data_index_2] > threshold_2:
                data_points_above_both_thresholds += 1
            else:
                data_points_above_both_thresholds = 0
                start_index_of_continuity = current_index + 1
            current_index += 1

        if data_points_above_both_thresholds == win_length:
            return start_index_of_continuity
    except IndexError:
        raise Exception(INDEX_EXCEPTION_MESSAGE)


def search_multi_continuity_within_range(data, index_begin, index_end, threshold_low,
                                         threshold_high, win_length, swing_to_analyze=None):
    validate_params(locals())
    swing_to_analyze = set_data(swing_to_analyze)
    query_index = map_data_to_index(data)

    ranges_meeting_criteria = []

    start_index_of_continuity = index_begin
    current_index = index_begin
    data_points_within_range = 0

    try:
        while current_index <= index_end:
            if threshold_high > swing_to_analyze[current_index][query_index] > threshold_low:
                data_points_within_range += 1
                if data_points_within_range == win_length:
                    ranges_meeting_criteria.append([start_index_of_continuity, current_index])
                    data_points_within_range -= 1
                    start_index_of_continuity += 1
            else:
                data_points_within_range = 0
                start_index_of_continuity = current_index + 1
            current_index += 1
        return ranges_meeting_criteria
    except IndexError:
        raise Exception(INDEX_EXCEPTION_MESSAGE)


def validate_params(params):
    param_validations = {
        'threshold': validate_is_number,
        'index_begin': validate_non_negative_number,
        'index_end': validate_non_negative_number,
        'win_length': validate_positive_number,
        'threshold_low': validate_is_number,
        'threshold_high': validate_is_number,
        'threshold_1': validate_is_number,
        'threshold_2': validate_is_number,
    }
    for param_name, param_value in params.iteritems():
        if param_validations.get(param_name):
            param_validations[param_name](param_value, param_name)


def validate_is_number(param, param_name):
    if type(param) not in [float, int]:
        raise Exception('{} must be a float or int!'.format(param_name))


def validate_non_negative_number(param, param_name):
    validate_is_number(param, param_name)
    if param < 0:
        raise Exception('{} must be zero or greater!'.format(param_name))


def validate_positive_number(param, param_name):
    validate_is_number(param, param_name)
    if param <= 0:
        raise Exception('{} must be greater than zero!'.format(param_name))


def set_data(swing_to_analyze):
    if swing_to_analyze is None:
        return swing_data
    return swing_to_analyze


def map_data_to_index(data):
    column_mapping = {
        'timeStamp': 0,
        'ax': 1,
        'ay': 2,
        'az': 3,
        'wx': 4,
        'wy': 5,
        'wz': 6,
    }
    try:
        return column_mapping[data]
    except KeyError:
        raise Exception('data must be one of {}'.format(','.join(column_mapping.keys())))
