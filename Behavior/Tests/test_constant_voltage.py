from Utilities.Waveform.waveform import Waveform
from simulation_runner import *
from Utilities.Waveform.waveform_assertions import *
from unittest import TestCase
import os


class TestConstantVoltage(TestCase):

    def test_constant_voltage_mode(self):
        params = {
            "RLoad": "1e12",
            "Vset": "5",
            "Iset": "1",
            "Vin": "12",
        }



        assert_settles(waveforms['V(out)'],
                       value=5,
                       accuracy=1e-3,
                       min_duration=1e-3,
                       before=5e-3)
