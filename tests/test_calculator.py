import math
import unittest
from calculator import calculate_sgpa, calculate_cgpa
from grading_system import grade_from_percentage


class CalculatorTests(unittest.TestCase):
    def test_sgpa_credit_weighted(self):
        self.assertAlmostEqual(calculate_sgpa([4, 3], [9, 8]), 8.5714285714)

    def test_cgpa_credit_weighted(self):
        self.assertAlmostEqual(calculate_cgpa([8, 9], [20, 24]), 8.5454545454)

    def test_rejects_empty_and_mismatched_inputs(self):
        with self.assertRaises(ValueError): calculate_sgpa([], [])
        with self.assertRaises(ValueError): calculate_sgpa([3], [8, 9])

    def test_rejects_invalid_ranges(self):
        with self.assertRaises(ValueError): calculate_sgpa([0], [8])
        with self.assertRaises(ValueError): calculate_sgpa([3], [11])
        with self.assertRaises(ValueError): calculate_cgpa([10.1], [20])

    def test_rejects_nan_and_infinity(self):
        for bad in (math.nan, math.inf, -math.inf):
            with self.assertRaises(ValueError): calculate_sgpa([3], [bad])
            with self.assertRaises(ValueError): grade_from_percentage(bad)

    def test_grade_boundaries(self):
        self.assertEqual(grade_from_percentage(90), ("A+", 10))
        self.assertEqual(grade_from_percentage(40), ("E", 4))
        self.assertEqual(grade_from_percentage(39.99), ("F", 0))
        self.assertEqual(grade_from_percentage(100), ("A+", 10))


if __name__ == "__main__":
    unittest.main()
