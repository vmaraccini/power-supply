def settle_time(waveform, value, accuracy, min_duration=0):
    """
    Computes the settling time of a Waveform to a given value within some accuracy and minimum duration.

    :param waveform: The Waveform to analyse
    :param value: The value to check convergence to
    :param accuracy: The maximum allowed deviation from the value to consider convergence
    :param min_duration: The minimum duration (in the Waveform timescale) to consider convergence
    :return: A tuple of the start time and the duration of the convergence.
    """
    value_ranges = waveform.contiguous_value_within((value - accuracy, value + accuracy))

    if len(value_ranges) == 0:
        raise Exception(
            "Failed to find convergence to {} with {} accuracy".format(value, accuracy))

    for value_range in value_ranges:
        start = value_range.timestamps[0]
        end = value_range.timestamps[-1]
        if (end - start) < min_duration:
            continue

        return start, end - start

    raise Exception("Convergence didn't last at least {}".format(min_duration))


def assert_settles(waveform, value, accuracy, min_duration=0, before=float("inf")):
    """
    Asserts whether a Waveform settles to a given value with a given accuracy and minimum duration before a
    maximum time.

    :param waveform: The Waveform to analyse
    :param value: The value to check convergence to
    :param accuracy: The maximum allowed deviation from the value to consider convergence
    :param min_duration: The minimum duration (in the Waveform timescale) to consider convergence
    :param before: The maximum timestamp to fulfill the convergence requirements
    """
    time_range = waveform[(0, before)]
    value_range = time_range.value_within((value - accuracy, value + accuracy))

    if len(value_range) == 0:
        raise Exception(
            "Failed to find convergence to {} before time {} with {} accuracy".format(value, before, accuracy))

    start = value_range.timestamps[0]
    if start > before:
        raise Exception("Convergence took longer than {}".format(before))

    end = value_range.timestamps[-1]
    if (end - start) < min_duration:
        raise Exception("Convergence didn't last at least {}".format(min_duration))


def assert_bound(waveform, lower=float("-inf"), upper=float("inf")):
    """
    Asserts whether a Waveform's values are lower and upper bound to the given values.

    :param waveform: The Waveform to analyse
    :param lower: The lower boundary
    :param upper: The upper boundary
    """
    value_range = waveform.value_within((lower, upper))

    if len(value_range) != len(waveform):
        raise Exception("Waveform not entirely bound to ({}, {})".format(lower, upper))


def assert_in_range(waveform, range):
    """
    Asserts whether a Waveform'' values are withni a given range tuple.

    :param waveform: The Waveform to analyse
    :param range: A tuple containing the lower and upper bounds, respectively
    """
    assert_bound(waveform, lower=range[0], upper=range[1])
