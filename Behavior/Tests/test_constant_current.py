from Utilities.Waveform.waveform import Waveform
from simulation_runner import *
from Utilities.Waveform.waveform_assertions import *
from unittest import TestCase

class TestConstantCurrent(TestCase):
    v_set = 12
    i_set = 0.5
    max_ripple = 2e-3
    max_overshoot = 0.2
    max_settle_time = 5e-3
    current_limit_range = (2e-3, 7e-3)

    def test_constant_current_mode_1_Ohm(self):
        load = 1
        i_set = self.i_set / load
        params = {
            "RLoad": load,
            "Vset": self.v_set,
            "Iset": i_set,
            "Ilow": 0
        }

        waveforms = SimulationRunner().simulate(params=params)
        output_current = waveforms['I(R2)']

        # Current settling time and ripple
        start = self.current_limit_range[0]
        assert_settles(output_current[start:],
                       value=i_set,
                       accuracy=self.max_ripple,
                       min_duration=1e-3,
                       before=self.max_settle_time + start)

        # Max overshoot
        assert_bound(output_current,
                     lower=0,
                     upper=self.i_set + self.max_overshoot)

        # Current limit down to 0
        start = self.current_limit_range[1]
        assert_settles(output_current[start:],
                       value=0,
                       accuracy=self.max_ripple,
                       min_duration=1e-3,
                       before=self.max_settle_time + start)

