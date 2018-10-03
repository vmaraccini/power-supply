import matplotlib as mpl

mpl.use('Agg')

import matplotlib.pyplot as plt
from inspect import getframeinfo, stack
import os


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


def assert_settles(waveform, value, accuracy, min_duration=0, before=float("inf"), generate_images=True):
    """
    Asserts whether a Waveform settles to a given value with a given accuracy and minimum duration before a
    maximum time.

    :param waveform: The Waveform to analyse
    :param value: The value to check convergence to
    :param accuracy: The maximum allowed deviation from the value to consider convergence
    :param min_duration: The minimum duration (in the Waveform timescale) to consider convergence
    :param before: The maximum timestamp to fulfill the convergence requirements
    :param generate_images: Sets whether to generate debug images
    """
    time_range = waveform[(0, before)]
    value_ranges = time_range.contiguous_value_within((value - accuracy, value + accuracy))

    if len(value_ranges) == 0:
        raise WaveformAssertionException(
            "Failed to find convergence to {} before time {} with {} accuracy for at least {}".format(value,
                                                                                                      before,
                                                                                                      accuracy,
                                                                                                      min_duration))

    def __image(failed=True):
        if generate_images:
            __save_settle_image(time_range, value=value, accuracy=accuracy, failed=failed)

    for value_range in value_ranges:
        start = value_range.timestamps[0]
        end = value_range.timestamps[-1]
        if (end - start) < min_duration or start > before:
            continue

        __image(failed=False)
        return start, end - start

    __image()

    actual_settle_time, _ = settle_time(waveform, value=value, accuracy=accuracy, min_duration=min_duration)
    raise WaveformAssertionException(
        "Convergence didn't last at least {} or\
         did not occur before {}. Actual settling time: {}".format(min_duration, before, actual_settle_time))


def assert_bound(waveform, lower=float("-inf"), upper=float("inf"), ignore_before=1e-7, generate_images=True):
    """
    Asserts whether a Waveform's values are lower and upper bound to the given values.

    :param waveform: The Waveform to analyse
    :param lower: The lower boundary
    :param upper: The upper boundary
    :param ignore_before: Sets the minimum timestamp before which bounds are not checked.
     This is useful to ignore spurious values at the beginning of the simulation.
    :param generate_images: Sets whether to generate debug images
    """
    if ignore_before is not None:
        waveform = waveform[ignore_before:]

    if len(waveform.timestamps) == 0:
        raise WaveformAssertionException("No entries in waveform!")

    value_range = waveform.value_within((lower, upper))

    def __image(failed=True):
        if generate_images:
            __save_image(waveform, max(min(waveform.values), lower), min(upper, max(waveform.values)),
                         margin=(min(waveform.values) + max(waveform.values)) / 10.0,
                         failed=failed)

    if len(value_range.timestamps) == 0:
        __image()
        raise WaveformAssertionException("No timestamps where waveform is bound to ({}, {}).".format(lower, upper))

    if len(value_range) != len(waveform):
        outliers = waveform.value_within((float("-inf"), lower)).timestamps + \
                   waveform.value_within((upper, float("inf"))).timestamps

        __image()

        array_desc = "{}...{}".format(outliers[0:5], outliers[-5:]) if len(outliers) > 10 else str(outliers)
        raise WaveformAssertionException("Waveform not entirely bound to ({}, {}).\nExamples: {}"
                                         .format(lower, upper, array_desc))

    __image(failed=False)


def assert_in_range(waveform, range, ignore_before=1e-7):
    """
    Asserts whether a Waveform'' values are withni a given range tuple.

    :param waveform: The Waveform to analyse
    :param range: A tuple containing the lower and upper bounds, respectively
    """
    assert_bound(waveform, lower=range[0], upper=range[1], ignore_before=ignore_before)


def __save_settle_image(waveform, value, accuracy, failed=True):
    __save_image(waveform,
                 min_y=value - accuracy,
                 max_y=value + accuracy,
                 margin=3 * accuracy,
                 failed=failed)


def __save_image(waveform, min_y, max_y, margin=0.0, failed=True):
    # Find calling test by searching stacktrace
    test_stack_index = next(i for (i, x) in enumerate(stack()) if 'test_' in getframeinfo(x[0]).function)
    caller = getframeinfo(stack()[test_stack_index][0])

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(waveform.timestamps, waveform.values)
    ax.fill_between([0, max(waveform.timestamps)], [min_y, min_y], [max_y, max_y],
                    facecolor='green', alpha=0.5)

    y_lim = ax.get_ylim()
    ax.set_ylim([max(min_y - margin, y_lim[0]), min(max_y + margin, y_lim[1])])

    filename = os.path.basename(caller.filename)
    test_path = os.path.dirname(caller.filename)
    subdir = "assertion-failures" if failed else "assertion-passes"

    filename = "{}/{}/{}-{}-L{}.png".format(test_path, subdir, caller.function, filename, caller.lineno)
    try:
        os.makedirs(os.path.dirname(os.path.abspath(filename)))
    except OSError:
        pass

    fig.savefig(filename)
