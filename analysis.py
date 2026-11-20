"""Pandas-based result viewing and performance analysis."""
import pandas as pd
from data_manager import get_subjects, get_semesters


def show_subject_results(roll_no):
    df = get_subjects(roll_no)
    if df.empty:
        print("No subject records found for this roll number.")
        return
    columns = ["semester", "subject_code", "subject_name", "credits", "total_marks", "maximum_marks", "grade", "grade_point"]
    print(df.loc[:, columns].sort_values(["semester", "subject_code"]).to_string(index=False))


def show_performance(roll_no):
    subjects = get_subjects(roll_no)
    semesters = get_semesters(roll_no)
    if subjects.empty and semesters.empty:
        print("No saved results for this roll number.")
        return
    print("\n========== PERFORMANCE ANALYSIS ==========")
    if not subjects.empty:
        points = pd.to_numeric(subjects["grade_point"], errors="coerce").dropna()
        credits = pd.to_numeric(subjects["credits"], errors="coerce").dropna()
        if not points.empty:
            print(f"Highest grade point: {points.max():g}")
            print(f"Lowest grade point : {points.min():g}")
        print("Total subject records:", len(subjects))
        print("Total subject credits:", f"{credits.sum():g}")
    if not semesters.empty:
        semesters = semesters.copy()
        semesters["semester"] = pd.to_numeric(semesters["semester"], errors="coerce")
        semesters = semesters.sort_values("semester")
        print("\nSemester-wise SGPA:")
        print(semesters[["semester", "total_credits", "sgpa"]].to_string(index=False))
        credit_values = pd.to_numeric(semesters["total_credits"], errors="coerce")
        sgpa_values = pd.to_numeric(semesters["sgpa"], errors="coerce")
        valid = credit_values.notna() & sgpa_values.notna() & (credit_values > 0)
        if valid.any():
            overall = (sgpa_values[valid] * credit_values[valid]).sum() / credit_values[valid].sum()
            print(f"\nOverall CGPA: {overall:.2f}")