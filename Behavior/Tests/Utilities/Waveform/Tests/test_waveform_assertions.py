from unittest import TestCase
from waveform import Waveform
from waveform_assertions import *


class TestWaveformAssertions(TestCase):
    waveform = Waveform(timestamps=[0, 1, 2, 3, 4], values=[0, 3, 2, 2.2, 1.8])

    def test_assert_settles(self):
        assert_settles(self.waveform, value=2, accuracy=0.2, length=2)
        assert_settles(self.waveform, value=2, accuracy=0.2, length=2, within=4)

        self.assertRaises(Exception, lambda: assert_settles(self.waveform, value=2, accuracy=0.2, length=2, within=1))
        self.assertRaises(Exception, lambda: assert_settles(self.waveform, value=1, accuracy=0.2, length=2, within=3))
        self.assertRaises(Exception, lambda: assert_settles(self.waveform, value=2, accuracy=0.1, length=2, within=3))
        self.assertRaises(Exception, lambda: assert_settles(self.waveform, value=2, accuracy=0.2, length=3, within=3))
        self.assertRaises(Exception, lambda: assert_settles(self.waveform, value=2, accuracy=0.2, length=2, within=1))

    def test_assert_bound(self):
        assert_bound(self.waveform, lower=0)
        assert_bound(self.waveform, upper=3)
        assert_bound(self.waveform, lower=0, upper=3)
        self.assertRaises(Exception, lambda: assert_bound(self.waveform, lower=1))
        self.assertRaises(Exception, lambda: assert_bound(self.waveform, upper=2))

    def test_assert_in_range(self):
        assert_in_range(self.waveform, (0, 3))
        self.assertRaises(Exception, lambda: assert_in_range(self.waveform, (0, 2)))
        self.assertRaises(Exception, lambda: assert_in_range(self.waveform, (1, 5)))

    def test_settle_time(self):
        waveform = Waveform(timestamps=[0, 1, 2, 3, 4, 5, 6, 7], values=[0, 3, 2, 2.2, 1.8, 2.1, 1.9, 2])
        self.assertEqual(settle_time(waveform, value=2, accuracy=0.2), (2, 5))
        self.assertEqual(settle_time(waveform, value=2, accuracy=0.1), (2, 0))
        self.assertEqual(settle_time(waveform, value=2, accuracy=0.1, min_length=1), (5, 2))
