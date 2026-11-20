"""Validated, vectorised SGPA and CGPA calculations."""
from __future__ import annotations
import numpy as np


def _numeric_array(values, label: str) -> np.ndarray:
    try:
        array = np.asarray(values, dtype=float)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{label} must contain numeric values.") from exc
    if array.ndim != 1 or array.size == 0:
        raise ValueError(f"{label} must be a non-empty one-dimensional list.")
    if not np.all(np.isfinite(array)):
        raise ValueError(f"{label} cannot contain NaN or infinity.")
    return array


def calculate_sgpa(credits, grade_points) -> float:
    """Calculate credit-weighted SGPA: sum(credit × grade point) / sum(credits)."""
    credits = _numeric_array(credits, "Credits")
    points = _numeric_array(grade_points, "Grade points")
    if credits.size != points.size:
        raise ValueError("Credits and grade points must contain the same number of values.")
    if np.any(credits <= 0):
        raise ValueError("Every subject credit must be greater than zero.")
    if np.any((points < 0) | (points > 10)):
        raise ValueError("Grade points must be between 0 and 10.")
    return float(np.dot(credits, points) / credits.sum())


def calculate_cgpa(sgpas, semester_credits) -> float:
    """Calculate credit-weighted CGPA from semester SGPAs and credits."""
    sgpas = _numeric_array(sgpas, "SGPA values")
    credits = _numeric_array(semester_credits, "Semester credits")
    if sgpas.size != credits.size:
        raise ValueError("SGPA and semester-credit lists must have equal lengths.")
    if np.any((sgpas < 0) | (sgpas > 10)):
        raise ValueError("Each SGPA must be between 0 and 10.")
    if np.any(credits <= 0):
        raise ValueError("Semester credits must be greater than zero.")
    return float(np.dot(sgpas, credits) / credits.sum())