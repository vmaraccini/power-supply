from Utilities.Waveform.waveform import Waveform
from Utilities.LTspiceCLI.simulate import *
from Utilities.LTspiceCLI.parse import *


class SimulationRunner:
    def __init__(self, config_filepath="Tests/config.json", filename="Spice/PowerSupply.asc"):
        with open(config_filepath) as config_file:
            self.config = json.loads(config_file.read())
        self.filename = filename

    def simulate(self, params={}):
        simulator = Simulator(**self.config)

        filename = os.path.realpath(self.filename)
        result_file = simulator.simulate(filename, params=params)
        
        parser = Parser()
        parser.parse(result_file)

        json = parser.serialize()
        return Waveform.parse(json)
