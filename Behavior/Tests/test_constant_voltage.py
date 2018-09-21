from Utilities.Waveform.waveform import Waveform
from simulation_runner import *
from Utilities.Waveform.waveform_assertions import *
from unittest import TestCase

class TestConstantVoltage(TestCase):
    v_set = 5
    max_ripple = 1e-3
    max_overshoot = 0.2
    max_settle_time = 5e-3

    def test_constant_voltage_mode(self):
        params = {
            "RLoad": "1e12",
            "Vset": str(self.v_set)
        }

        waveforms = SimulationRunner().simulate(params=params)
        output_voltage = waveforms['V(out)']

        assert_settles(output_voltage,
                       value=self.v_set,
                       accuracy=self.max_ripple,
                       min_duration=1e-3,
                       before=self.max_settle_time)

        assert_bound(output_voltage,
                     lower=0,
                     upper=self.v_set + self.max_overshoot)

        settle_start = settle_time(output_voltage,
                                   value=self.v_set,
                                   accuracy=self.max_ripple,
                                   min_duration=1e-3)

        assert_bound(output_voltage[settle_start:],
                     lower=self.v_set - self.max_ripple,
                     upper=self.v_set - self.max_ripple)
