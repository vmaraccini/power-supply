from unittest import TestCase
from waveform import Waveform
from waveform_assertions import *


class TestWaveformAssertions(TestCase):
    waveform = Waveform(timestamps=[0, 1, 2, 3, 4], values=[0, 3, 2, 2.2, 1.8])

    def test_assert_settles(self):
        assert_settles(self.waveform, value=2, accuracy=0.2, min_duration=2, generate_images=False)
        assert_settles(self.waveform, value=2, accuracy=0.2, min_duration=2, before=4, generate_images=False)

        self.assertRaises(Exception,
                          lambda: assert_settles(self.waveform, value=2, accuracy=0.2, min_duration=2, before=1,
                                                 generate_images=False))
        self.assertRaises(Exception,
                          lambda: assert_settles(self.waveform, value=1, accuracy=0.2, min_duration=2, before=3,
                                                 generate_images=False))
        self.assertRaises(Exception,
                          lambda: assert_settles(self.waveform, value=2, accuracy=0.1, min_duration=2, before=3,
                                                 generate_images=False))
        self.assertRaises(Exception,
                          lambda: assert_settles(self.waveform, value=2, accuracy=0.2, min_duration=3, before=3,
                                                 generate_images=False))
        self.assertRaises(Exception,
                          lambda: assert_settles(self.waveform, value=2, accuracy=0.2, min_duration=2, before=1,
                                                 generate_images=False))

    def test_assert_bound(self):
        assert_bound(self.waveform, lower=0, generate_images=False)
        assert_bound(self.waveform, upper=3, generate_images=False)
        assert_bound(self.waveform, lower=0, upper=3, generate_images=False)
        assert_bound(self.waveform, lower=1, ignore_before=1, generate_images=False)
        self.assertRaises(Exception,
                          lambda: assert_bound(self.waveform, lower=1, ignore_before=None, generate_images=False))
        self.assertRaises(Exception,
                          lambda: assert_bound(self.waveform, upper=2, ignore_before=None, generate_images=False))

    def test_assert_in_range(self):
        assert_in_range(self.waveform, (0, 3), generate_images=False)
        assert_in_range(self.waveform, (1, 5), ignore_before=1, generate_images=False)
        self.assertRaises(Exception, lambda: assert_in_range(self.waveform, (0, 2)), generate_images=False)
        self.assertRaises(Exception, lambda: assert_in_range(self.waveform, (1, 5)), ignore_before=None,
                          generate_images=False)

    def test_settle_time(self):
        waveform = Waveform(timestamps=[0, 1, 2, 3, 4, 5, 6, 7], values=[0, 3, 2, 2.2, 1.8, 2.1, 1.9, 2])
        self.assertEqual(settle_time(waveform, value=2, accuracy=0.2), (2, 5))
        self.assertEqual(settle_time(waveform, value=2, accuracy=0.1), (2, 0))
        self.assertEqual(settle_time(waveform, value=2, accuracy=0.1, min_duration=1), (5, 2))
