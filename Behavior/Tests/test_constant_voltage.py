from Utilities.Waveform.waveform import Waveform
from simulation_runner import *
from Utilities.Waveform.waveform_assertions import *
from unittest import TestCase
from assert_component_ratings import *


class TestConstantVoltage(TestCase):
    v_set = 5
    wait_duration = 50e-3
    max_ripple = 10e-3
    max_overshoot = 0.2
    max_settle_time = 30e-3

    def test_constant_voltage_mode_open(self):
        params = {
            "RLoad": "1e12",
            "Vset": self.v_set,
            "Iset": 10,
            "Istart": 0,
            "Von": self.wait_duration,
            "Ion": self.wait_duration,
        }

        waveforms = SimulationRunner().simulate(params=params)
        output_voltage = waveforms['V(out)']

        assert_settles(output_voltage,
                       value=self.v_set,
                       accuracy=self.max_ripple,
                       min_duration=1e-3,
                       before=self.max_settle_time,
                       label="Output settle open circuit")

        assert_bound(output_voltage,
                     lower=0,
                     upper=self.v_set + self.max_overshoot,
                     label="Max output voltage overshoot open circuit")

        settle_start, _ = settle_time(output_voltage,
                                      value=self.v_set,
                                      accuracy=self.max_ripple,
                                      min_duration=1e-3)

        self.assertLess(settle_start, self.max_settle_time)

        assert_bound(output_voltage[settle_start:self.wait_duration],
                     lower=self.v_set - self.max_ripple,
                     upper=self.v_set + self.max_ripple,
                     label="Max output voltage ripple open circuit")

        assert_components(waveforms)

    def test_constant_voltage_mode_10_ohm(self):
        params = {
            "RLoad": "10",
            "Vset": self.v_set,
            "Iset": 10,
            "Istart": 0,
            "Von": self.wait_duration,
            "Ion": self.wait_duration
        }

        waveforms = SimulationRunner().simulate(params=params)
        output_voltage = waveforms['V(out)']

        assert_settles(output_voltage,
                       value=self.v_set,
                       accuracy=self.max_ripple,
                       min_duration=1e-3,
                       before=self.max_settle_time,
                       label="Output settling 10 ohm")

        assert_bound(output_voltage,
                     lower=0,
                     upper=self.v_set + self.max_overshoot,
                     label="Max output voltage ripple overshoot 10 ohm")

        settle_start, _ = settle_time(output_voltage,
                                      value=self.v_set,
                                      accuracy=self.max_ripple,
                                      min_duration=1e-3)

        self.assertLess(settle_start, self.max_settle_time)

        assert_bound(output_voltage[settle_start:self.wait_duration],
                     lower=self.v_set - self.max_ripple,
                     upper=self.v_set + self.max_ripple,
                     label="Max output voltage ripple 10 ohm")

        assert_components(waveforms)
