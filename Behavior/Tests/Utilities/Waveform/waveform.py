import json


class Waveform:
    timestamps = []
    values = []

    @staticmethod
    def parse(json_string):
        dictionary = json.loads(json_string)
        time = dictionary['time']
        return {k: Waveform(timestamps=time, values=v) for (k, v) in dictionary.iteritems()}

    def __init__(self, timestamps, values):
        if len(timestamps) == 0 or len(values) == 0:
            return

        sorted_zip = sorted(zip(timestamps, values), lambda x, y: x[0] > y[0])
        sorted_time, sorted_values = map(list, zip(*sorted_zip))
        self.timestamps = sorted_time
        self.values = sorted_values

    def mapping(self, predicate):
        return Waveform(*zip(*map(predicate, zip(self.timestamps, self.values)) or [[], []]))

    def matching(self, predicate):
        return Waveform(*zip(*filter(predicate, zip(self.timestamps, self.values))) or [[], []])

    def contiguous_matches(self, predicate):
        def append_contiguous(curr, el):
            if len(curr) == 0:
                curr.append([el])
            elif curr[-1][-1][0] + 1 == el[0]:
                curr[-1].append(el)
            else:
                curr.append([el])
            return curr

        timestamps, values = zip(*filter(predicate, zip(enumerate(self.timestamps), self.values)))
        contiguous_groups = reduce(append_contiguous, timestamps, [])
        indexes = [[y[0] for y in x] for x in contiguous_groups]
        sequences = map(lambda x: [(self.timestamps[y], self.values[y]) for y in x], indexes)
        return [Waveform(*zip(*x)) for x in sequences]

    def value_within(self, range):
        return self.matching(lambda (x, y): range[0] <= y <= range[1])

    def contiguous_value_within(self, range):
        return self.contiguous_matches(lambda (x, y): range[0] <= y <= range[1])

    def interpolating(self, timestamp):
        if timestamp in self.timestamps:
            return self.values[self.timestamps.index(timestamp)]
        else:
            index = next(x[0] for x in enumerate(self.timestamps) if x[1] > timestamp)
            if index == 0 or index == len(self.timestamps) - 1:
                return self.values[index]

            progress = (self.timestamps[index] - timestamp) / (self.timestamps[index] - self.timestamps[index - 1])
            final = self.values[index]
            initial = self.values[index - 1]

            return initial + (final - initial) * progress

    def __len__(self):
        return len(self.timestamps)

    def __getitem__(self, item):
        if isinstance(item, (int, long, float)):
            return self.interpolating(item)
        elif isinstance(item, list):
            return self.matching(lambda (x, y): item in x)
        elif isinstance(item, tuple):
            return self.matching(lambda (x, y): item[0] <= x <= item[1])
