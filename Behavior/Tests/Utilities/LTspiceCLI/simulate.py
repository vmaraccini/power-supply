from subprocess import call
import re
import os


class Simulator:
    def __init__(self, executable_path, wine_args=[]):
        """
        Constructs a new Simulator instance.

        :param executable_path: The LTspice executable path
        :param wine_args: The wine command list, if required. Pass [] if using wine is not required
        (i.e.: if running on Windows)
        """
        self.executable_path = os.path.expanduser(executable_path)
        self.wine_args = wine_args

    def simulate(self, filename, params=None):
        """
        Runs the simulation on a given filename with the supplied parameters.

        :param filename: The schematic filename to run the simulation
        :param params: A dictionary containing the simulation parameters to override with the parameter names as keys
        """
        return self.run_with_parameters(filename, params, self.run_simulation)

    def run_simulation(self, filename):
        commands = [self.executable_path, "--ascii", "-b", "-run"]
        if len(self.wine_args) > 0:
            commands = self.wine_args + commands
            commands.append("z:" + filename)
        else:
            commands.append(filename)

        file_path = filename.rsplit(".", 1)[0]
        simulation_status = call(commands)
        if simulation_status != 0:
            log_path = file_path + ".log"
            command = ['tail', '-n', '50', log_path]
            call(command)
            raise RuntimeError('Simulation failed, code: {}'.format(simulation_status))

        return file_path + ".raw"

    def run_with_parameters(self, filename, params, func):
        if params is None:
            return func(filename)

        with open(filename, 'r') as file:
            lines = file.readlines()

        def replace_param(line, params):
            regex = re.compile(r".param (.*) .*")
            param_key = regex.search(line).group(1)
            if param_key in params:
                return re.sub(r'.param (.*) .*', r".param \1 {}".format(str(params[param_key])), line)
            else:
                return line

        result = map(lambda l: replace_param(l, params) if '.param' in l else l, lines)
        result_string = str.join('', result)
        new_filename = filename
        with open(new_filename, 'w') as file:
            file.write(result_string)

        return func(new_filename)
