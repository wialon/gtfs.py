TRUE_FALSE_OPTIONS = [0, 1]
YES_NO_UNKNOWN_OPTIONS = [0, 1, 2]

PICKUP_DROP_OFF_OPTIONS = [0, 1, 2, 3]


def not_none_or_empty(value):
    return value is not None and value != ''


def validate_true_false(number):
    return number in TRUE_FALSE_OPTIONS


def validate_pickup_drop_off_types(number):
    return number in PICKUP_DROP_OFF_OPTIONS


def validate_yes_no_unknown(number):
    return number is None or number in YES_NO_UNKNOWN_OPTIONS
