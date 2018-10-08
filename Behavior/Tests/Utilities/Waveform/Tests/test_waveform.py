from unittest import TestCase
from waveform import Waveform


class TestWaveform(TestCase):
    test_waveform = Waveform(timestamps=[0, 1, 2, 3], values=[4, 3, 2, 1])

    def test_mapping(self):
        mapped = self.test_waveform.mapping(lambda (x, y): (x * 2, y * 2))
        self.assertEqual(mapped.timestamps, [0, 2, 4, 6])
        self.assertEqual(mapped.values, [8, 6, 4, 2])

    def test_matching(self):
        matched = self.test_waveform.matching(lambda (x, y): (x > 1))
        self.assertEqual(matched.timestamps, [2, 3])
        self.assertEqual(matched.values, [2, 1])

    def test_contiguous_matching(self):
        waveform = Waveform(timestamps=[0, 1, 2, 3], values=[1, 3, 1, 1])
        matched = waveform.contiguous_value_within((0.9, 1.1))
        self.assertEqual(matched[0].timestamps, [0])
        self.assertEqual(matched[0].values, [1])

        self.assertEqual(matched[1].timestamps, [2, 3])
        self.assertEqual(matched[1].values, [1, 1])

    def test_value_within(self):
        full_range = self.test_waveform.value_within((-1, 5))
        self.assertEqual(full_range.timestamps, self.test_waveform.timestamps)
        self.assertEqual(full_range.values, self.test_waveform.values)

        within = self.test_waveform.value_within((1, 3))
        self.assertEqual(within.timestamps, [1, 2, 3])
        self.assertEqual(within.values, [3, 2, 1])

        within = self.test_waveform.value_within((2, 5))
        self.assertEqual(within.timestamps, [0, 1, 2])
        self.assertEqual(within.values, [4, 3, 2])

    def test_interpolating(self):
        self.assertAlmostEqual(self.test_waveform[0.5], 3.5, 5)

    def test_timerange(self):
        time_range = self.test_waveform[(0, 2)]
        self.assertEqual(time_range.timestamps, [0, 1, 2])
        self.assertEqual(time_range.values, [4, 3, 2])

    def test_parse(self):
        json_string = open("Tests/sample.json", 'r').read()
        result = Waveform.parse(json_string)

        test_waveform = result["V(vref)"]
        self.assertIsNotNone(test_waveform)
        self.assertEqual(len(test_waveform), 13601)
        self.assertAlmostEqual(test_waveform[0], 0, places=6)
        self.assertAlmostEqual(test_waveform[1e-3], 4, places=6)

    def test_add(self):
        one = Waveform([0, 2, 4], [0, 2, 4])
        other = Waveform([0, 2, 4], [1, 3, 5])

        result = one + other
        self.assertEqual(result.timestamps, one.timestamps)
        self.assertEqual(result.values, [1, 5, 9])

    def test_add_interpolated(self):
        one = Waveform([0, 2, 4, 6], [0, 2, 4, 6])
        other = Waveform([1, 3, 5], [1, 3, 5])

        result = one + other
        self.assertEqual(result.timestamps, one.timestamps)
        map(lambda (x, y): self.assertAlmostEqual(x, y, places=6), zip(result.values, [1, 4, 8, 11]))

    def test_sub(self):
        one = Waveform([0, 2, 4], [0, 2, 4])
        other = Waveform([0, 2, 4], [1, 3, 5])

        result = one - other
        self.assertEqual(result.timestamps, one.timestamps)
        self.assertEqual(result.values, [-1, -1, -1])

    def test_sub_interpolated(self):
        one = Waveform([0, 2, 4, 6], [0, 2, 4, 6])
        other = Waveform([1, 3, 5], [1, 3, 5])

        result = one - other
        self.assertEqual(result.timestamps, one.timestamps)
        map(lambda (x, y): self.assertAlmostEqual(x, y, places=6), zip(result.values, [-1, 0, 0, 1]))

    def test_mul(self):
        one = Waveform([0, 2, 4], [0, 2, 4])
        other = Waveform([0, 2, 4], [1, 3, 5])

        result = one * other
        self.assertEqual(result.timestamps, one.timestamps)
        self.assertEqual(result.values, [0, 6, 20])

    def test_mul_scalar(self):
        result = 2.0 * self.test_waveform
        self.assertEqual(result.timestamps, self.test_waveform.timestamps)
        self.assertAlmostEqual(result.values, [8, 6, 4, 2], places=6)

        result = 2.0 * self.test_waveform
        self.assertEqual(self.test_waveform * 2, result)

    def test_mul_interpolated(self):
        one = Waveform([0, 2, 4, 6], [0, 2, 4, 6])
        other = Waveform([1, 3, 5], [1, 3, 5])

        result = one * other
        self.assertEqual(result.timestamps, one.timestamps)
        map(lambda (x, y): self.assertAlmostEqual(x, y, places=6), zip(result.values, [0, 4, 16, 30]))

    def test_div(self):
        one = Waveform([0, 2, 4], [0, 2, 4])
        other = Waveform([0, 2, 4], [1, 3, 5])

        result = one / other
        self.assertEqual(result.timestamps, one.timestamps)
        self.assertEqual(result.values, [0, 2.0 / 3, 4.0 / 5])

    def test_div_scalar(self):
        result = 2.0 / self.test_waveform
        self.assertEqual(result.timestamps, self.test_waveform.timestamps)
        map(lambda (x, y): self.assertAlmostEqual(x, y, places=6), zip(result.values, [0.5, 2.0 / 3, 1, 2]))

    def test_rdiv_scalar(self):
        result = self.test_waveform / 0.5
        self.assertEqual(result.timestamps, self.test_waveform.timestamps)
        self.assertEqual(result.values, [8, 6, 4, 2])

    def test_div_interpolated(self):
        one = Waveform([0, 2, 4, 6], [0, 2, 4, 6])
        other = Waveform([1, 3, 5], [1, 3, 5])

        result = one / other
        self.assertEqual(result.timestamps, one.timestamps)
        map(lambda (x, y): self.assertAlmostEqual(x, y, places=6), zip(result.values, [0, 1, 1, 6.0 / 5]))
