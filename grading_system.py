"""Editable percentage-to-grade mapping for educational estimation only.

The bands below are carried forward from the supplied project. They are NOT
verified as the current ABES/AKTU grading ordinance. Check the applicable
academic regulations before relying on a result.
"""
from math import isfinite

GRADE_SCALE = [
    (90, 100, "A+", 10), (80, 90, "A", 9), (70, 80, "B+", 8),
    (60, 70, "B", 7), (50, 60, "C", 6), (45, 50, "D", 5),
    (40, 45, "E", 4), (0, 40, "F", 0),
]


def grade_from_percentage(percentage):
    """Return (letter grade, grade point) for a finite percentage in [0, 100]."""
    try:
        value = float(percentage)
    except (TypeError, ValueError) as exc:
        raise ValueError("Percentage must be numeric.") from exc
    if not isfinite(value) or not 0 <= value <= 100:
        raise ValueError("Percentage must be a finite number from 0 to 100.")
    for lower, upper, letter, point in GRADE_SCALE:
        if lower <= value < upper or (value == 100 and upper == 100):
            return letter, point
    raise ValueError("No grade band found. Check GRADE_SCALE configuration.")


def get_grade_description(letter):
    descriptions = {
        "A+": "Outstanding", "A": "Excellent", "B+": "Very Good",
        "B": "Good", "C": "Above Average", "D": "Average",
        "E": "Minimum grade in this configured scale", "F": "Fail",
    }
    return descriptions.get(letter, "Unknown")
