import json


class Waveform:
    timestamps = []
    values = []

    @staticmethod
    def parse(json_string):
        """
        Parses a JSON string into a dictionary of Waveform objects, indexed by their name.

        Note: The incoming JSON dictionary must at least contain one entry named `time`

        :param json_string: The input JSON string.
        :return: A dictionary of parsed Waveform objects
        """
        dictionary = json.loads(json_string)
        time = dictionary['time']
        return {k: Waveform(timestamps=time, values=v) for (k, v) in dictionary.iteritems()}

    def __init__(self, timestamps, values):
        if len(timestamps) == 0 or len(values) == 0:
            return

        sorted_zip = sorted(zip(timestamps, values), cmp=lambda x, y: x[0] > y[0])
        sorted_time, sorted_values = map(list, zip(*sorted_zip))
        self.timestamps = sorted_time
        self.values = sorted_values

    def mapping(self, mapping_fn):
        """
        Maps each element of the Waveform to a new Waveform by using a mapping function.

        :param mapping_fn: The two-argument function to be applied to the sequence.
        :return: A new Waveform with the result of mapping_fn applied to each element.
        """
        return Waveform(*zip(*map(mapping_fn, zip(self.timestamps, self.values)) or [[], []]))

    def matching(self, predicate):
        """
        Returns a new Waveform with all the elements matching a given predicate.

        Note: Does not enforce the return a contiguous Waveform.

        :param predicate: The predicate to use when selecting elements.
        :return: The new Waveform with only the elements that "passed" the predicate.
        """
        return Waveform(*zip(*filter(predicate, zip(self.timestamps, self.values))) or [[], []])

    def contiguous_matches(self, predicate):
        """
        Returns a list of all the contiguous matches of a predicate

        :param predicate: The predicate to use when selecting elements.
        :return: A list of new Waveforms with only the elements that "passed" the predicate for each contiguous section.
        """

        def append_contiguous(curr, el):
            if len(curr) == 0:
                curr.append([el])
            elif curr[-1][-1][0] + 1 == el[0]:
                curr[-1].append(el)
            else:
                curr.append([el])
            return curr

        filtered = filter(predicate, zip(enumerate(self.timestamps), self.values))
        if len(filtered) == 0:
            return []

        timestamps, values = zip(*filtered)
        contiguous_groups = reduce(append_contiguous, timestamps, [])
        indexes = [[y[0] for y in x] for x in contiguous_groups]
        sequences = map(lambda x: [(self.timestamps[y], self.values[y]) for y in x], indexes)
        return [Waveform(*zip(*x)) for x in sequences]

    def value_within(self, range):
        """
        Returns a new Waveform with all the elements whose value are within the given range.

        Note: Does not enforce the return a contiguous Waveform.

        :param range: The minimum and maximum values to select within the Waveform, respectively.
        :return: A new Waveform with only the elements within the passed range.
        """
        return self.matching(lambda (x, y): range[0] <= y <= range[1])

    def contiguous_value_within(self, range):
        """
        Returns a list of new contiguous Waveform where all the elements are within the given range

        :param range: The minimum and maximum values to select within the Waveform, respectively.
        :return: A list of new Waveforms where each one is a contiguous segment where the values are within the range.
        """
        return self.contiguous_matches(lambda (x, y): range[0] <= y <= range[1])

    def interpolating(self, timestamp):
        """
        Returns the value of the Waveform at a given timestamp, interpolating if needed.

        :param timestamp: The queried timestamp
        :return: The value at the selected timestamp or a linear interpolation when the exact value is not available.
        """
        if timestamp in self.timestamps:
            return self.values[self.timestamps.index(timestamp)]
        else:
            if timestamp > max(self.timestamps):
                return self.values[-1]

            index = next(x[0] for x in enumerate(self.timestamps) if x[1] > timestamp)
            if index == 0:
                return self.values[index]

            progress = 1 - (self.timestamps[index] - timestamp) / \
                       float(self.timestamps[index] - self.timestamps[index - 1])
            final = self.values[index]
            initial = self.values[index - 1]

            return initial + (final - initial) * progress

    def __mul__(self, other):
        if isinstance(other, (int, long, float)):
            return Waveform(self.timestamps, [other * x for x in self.values])
        if isinstance(other, Waveform):
            if other.timestamps == self.timestamps:
                other_values = other.values
            else:
                other_values = map(lambda x: other[x], self.timestamps)
            return Waveform(self.timestamps, [x * y for (x, y) in zip(other_values, self.values)])
        else:
            raise Exception("Unimplemented multiplication between Waveform and {}".format(type(other)))

    __rmul__ = __mul__

    def __div__(self, other):
        if isinstance(other, (int, long, float)):
            return Waveform(self.timestamps, [float(x) / other for x in self.values])
        if isinstance(other, Waveform):
            if other.timestamps == self.timestamps:
                other_values = other.values
            else:
                other_values = map(lambda x: other[x], self.timestamps)
            return Waveform(self.timestamps, [float(x) / y for (x, y) in zip(self.values, other_values)])
        else:
            raise Exception("Unimplemented division between Waveform and {}".format(type(other)))

    def __rdiv__(self, other):
        if isinstance(other, (int, long, float)):
            return Waveform(self.timestamps, [other / float(x) for x in self.values])
        if isinstance(other, Waveform):
            if other.timestamps == self.timestamps:
                other_values = other.values
            else:
                other_values = map(lambda x: other[x], self.timestamps)
            return Waveform(self.timestamps, [float(x) / y for (x, y) in zip(self.values, other_values)])
        else:
            raise Exception("Unimplemented division between Waveform and {}".format(type(other)))

    def __add__(self, other):
        if isinstance(other, Waveform):
            if other.timestamps == self.timestamps:
                other_values = other.values
            else:
                other_values = map(lambda x: other[x], self.timestamps)
            return Waveform(self.timestamps, [sum(x) for x in zip(other_values, self.values)])
        else:
            raise Exception("Unimplemented add between Waveform and {}".format(type(other)))

    def __sub__(self, other):
        return self + Waveform(other.timestamps, [-x for x in other.values])

    def __len__(self):
        return len(self.timestamps)

    def __eq__(self, other):
        if isinstance(other, Waveform):
            return other.values == self.values and other.timestamps == self.timestamps
        return False

    def __abs__(self):
        return Waveform(self.timestamps, [abs(x) for x in self.values])

    def __getitem__(self, item):
        if isinstance(item, (int, long, float)):
            return self.interpolating(item)
        elif isinstance(item, list):
            return self.matching(lambda (x, y): x in item)
        elif isinstance(item, slice):
            return self.matching(lambda (x, y): (item.start or float("-inf")) <= x <= (item.stop or float("inf")))
        elif isinstance(item, tuple):
            return self.matching(lambda (x, y): item[0] <= x <= item[1])
