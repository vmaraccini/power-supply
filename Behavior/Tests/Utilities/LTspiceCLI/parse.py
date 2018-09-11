import numpy as np
import json


def next_in(seq, token):
    return (x for x in seq if x.startswith(token)).next()


def index_in(seq, token):
    return seq.index(next_in(seq, token))


def get_value(seq, token):
    return next_in(seq, token)[len(token):]


def get_int(seq, token):
    return int(get_value(seq, token))


class Parser:
    n_points = 0
    n_variables = 0

    data = {}

    def __init__(self):
        pass

    def parse(self, filename):
        """
        Parses an ASCII .raw simulation output file into a dictionary where the keys are the simulation variables.

        :param filename: The ASCII .raw simulation output.
        :return: A dictionary where the keys are the simulation variables and the values are arrays containing all the
        simulation variable values.
        """
        with open(filename, 'r') as file:
            lines = file.readlines()

        n_variables_token = "No. Variables: "
        n_points_token = "No. Points: "
        variables_token = "Variables:"
        values_token = "Values:"

        self.n_variables = get_int(lines, n_variables_token)
        self.n_points = get_int(lines, n_points_token)

        variables_start = index_in(lines, variables_token)
        variables = lines[variables_start + 1: variables_start + self.n_variables + 1]

        values_start = index_in(lines, values_token)
        values = np.array(lines[values_start + 1: values_start + self.n_variables * self.n_points + 1])
        values.resize((self.n_points, self.n_variables))
        values = np.transpose(values)

        data_keys = [v.strip().split('\t')[1] for v in variables]
        data_values = [[float(val.strip().split('\t')[-1]) for val in var] for var in values]
        self.data = dict(zip(data_keys, data_values))

    def serialize(self):
        """
        Returns the simulation dictionary serialized into a JSON string.

        Note: Must be called after `parse`.

        :return: The serialized JSON string
        """
        return json.dumps(self.data)
