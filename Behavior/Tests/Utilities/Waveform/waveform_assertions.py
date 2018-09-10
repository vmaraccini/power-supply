def settle_time(waveform, value, accuracy, min_length=0):
    valueranges = waveform.contiguous_value_within((value - accuracy, value + accuracy))

    if len(valueranges) == 0:
        raise Exception(
            "Failed to find convergence to {} with {} accuracy".format(value, accuracy))

    for valuerange in valueranges:
        start = valuerange.timestamps[0]
        end = valuerange.timestamps[-1]
        if (end - start) < min_length:
            continue

        return start, end-start

    raise Exception("Convergence didn't last at least {}".format(length))

def assert_settles(waveform, value, accuracy, length=0, within=float("inf")):
    timerange = waveform[(0, within)]
    valuerange = timerange.value_within((value - accuracy, value + accuracy))

    if len(valuerange) == 0:
        raise Exception(
            "Failed to find convergence to {} within time {} with {} accuracy".format(value, within, accuracy))

    start = valuerange.timestamps[0]
    if start > within:
        raise Exception("Convergence took longer than {}".format(within))

    end = valuerange.timestamps[-1]
    if (end - start) < length:
        raise Exception("Convergence didn't last at least {}".format(length))


def assert_bound(waveform, lower=float("-inf"), upper=float("inf")):
    valuerange = waveform.value_within((lower, upper))

    if len(valuerange) != len(waveform):
        raise Exception("Waveform not entirely bound to ({}, {})".format(lower, upper))


def assert_in_range(waveform, range):
    assert_bound(waveform, lower=range[0], upper=range[1])
