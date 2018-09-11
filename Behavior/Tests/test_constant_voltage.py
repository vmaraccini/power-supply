from Utilities.Waveform.waveform import Waveform
from Utilities.LTspiceCLI.simulate import *
from Utilities.LTspiceCLI.parse import *
from Utilities.Waveform.waveform_assertions import *
from unittest import TestCase
import os


class TestConstantVoltage(TestCase):
    config = {"executable_path": "/Applications/LTspice.app/Contents/MacOS/LTspice"}
    filename = "../PowerSupply.asc"

    def test_constant_voltage_mode(self):
        simulator = Simulator(**self.config)
        params = {
            "RLoad": "1e12",
            "Vset": "5",
            "Iset": "1",
            "Vin": "12",
        }

        dir = os.path.dirname(__file__)
        result_file = simulator.simulate(os.path.join(dir, self.filename), params=params)
        parser = Parser()
        parser.parse(result_file)

        json = parser.serialize()
        waveforms = Waveform.parse(json)

        assert_settles(waveforms['V(out)'],
                       value=5,
                       accuracy=1e-3,
                       min_duration=1e-3,
                       before=5e-3)
