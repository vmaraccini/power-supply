from Utilities.Waveform.waveform import Waveform
from Utilities.LTspiceCLI.simulate import *
from Utilities.LTspiceCLI.parse import *


class SimulationRunner:
    def __init__(self, config_filepath="Tests/config.json", filename="../Spice/PowerSupply.asc"):
        with open(config_filepath) as config_file:
            self.config = json.loads(config_file.read())
        self.filename = filename

    def simulate(self, params={}):
        simulator = Simulator(**self.config)
        curr_path = os.path.dirname(__file__)

        result_file = simulator.simulate(os.path.join(curr_path, self.filename), params=params)

        parser = Parser()
        parser.parse(result_file)

        json = parser.serialize()
        return Waveform.parse(json)
