class WaveformAssertionException(Exception):
    pass


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
        raise WaveformAssertionException(
            "Failed to find convergence to {} with {} accuracy".format(value, accuracy))

    for value_range in value_ranges:
        start = value_range.timestamps[0]
        end = value_range.timestamps[-1]
        if (end - start) < min_duration:
            continue

        return start, end - start

    raise WaveformAssertionException("Convergence didn't last at least {}".format(min_duration))


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
    value_ranges = time_range.contiguous_value_within((value - accuracy, value + accuracy))

    if len(value_ranges) == 0:
        raise WaveformAssertionException(
            "Failed to find convergence to {} before time {} with {} accuracy for at least {}".format(value,
                                                                                                      before,
                                                                                                      accuracy,
                                                                                                      min_duration))

    for value_range in value_ranges:
        start = value_range.timestamps[0]
        end = value_range.timestamps[-1]
        if (end - start) < min_duration or start > before:
            continue

        return start, end - start

    raise WaveformAssertionException(
        "Convergence didn't last at least {} or did not occur before {}".format(min_duration, before))


def assert_bound(waveform, lower=float("-inf"), upper=float("inf"), ignore_before=1e-7):
    """
    Asserts whether a Waveform's values are lower and upper bound to the given values.

    :param waveform: The Waveform to analyse
    :param lower: The lower boundary
    :param upper: The upper boundary
    :param ignore_before: Sets the minimum timestamp before which bounds are not checked.
     This is useful to ignore spurious values at the beginning of the simulation.
    """
    if ignore_before is not None:
        waveform = waveform[ignore_before:]

    value_range = waveform.value_within((lower, upper))

    if len(value_range) != len(waveform):
        outliers = waveform.value_within((float("-inf"), lower)).timestamps + \
                   waveform.value_within((upper, float("inf"))).timestamps

        array_desscription = "{}...{}".format(outliers[0:5], outliers[-5:]) if len(outliers) > 10 else str(outliers)
        raise WaveformAssertionException("Waveform not entirely bound to ({}, {}).\nExamples: {}"
                                         .format(lower, upper, array_desscription))


def assert_in_range(waveform, range, ignore_before=1e-7):
    """
    Asserts whether a Waveform'' values are withni a given range tuple.

    :param waveform: The Waveform to analyse
    :param range: A tuple containing the lower and upper bounds, respectively
    """
    assert_bound(waveform, lower=range[0], upper=range[1], ignore_before=ignore_before)
