"""Pandas CSV persistence with atomic writes and safe exports.

CSV files are plain text. Do not store passwords or publish personal student data.
"""
from __future__ import annotations
from pathlib import Path
import os
import tempfile
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"
SUBJECTS_FILE = DATA_DIR / "subjects.csv"
SEMESTERS_FILE = DATA_DIR / "semesters.csv"
STUDENTS_FILE = DATA_DIR / "students.csv"
SUBJECT_COLUMNS = ["roll_no", "student_name", "branch", "academic_year", "semester", "subject_code", "subject_name", "course_type", "credits", "internal_marks", "internal_max", "external_marks", "external_max", "total_marks", "maximum_marks", "percentage", "grade", "grade_point"]
SEMESTER_COLUMNS = ["roll_no", "student_name", "branch", "academic_year", "semester", "total_credits", "sgpa"]
STUDENT_COLUMNS = ["roll_no", "student_name", "branch", "academic_year"]


def initialize_storage():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    for path, columns in ((SUBJECTS_FILE, SUBJECT_COLUMNS), (SEMESTERS_FILE, SEMESTER_COLUMNS), (STUDENTS_FILE, STUDENT_COLUMNS)):
        if not path.exists():
            _atomic_csv_write(pd.DataFrame(columns=columns), path)


def _atomic_csv_write(frame: pd.DataFrame, path: Path):
    """Write beside target then replace it, reducing risk of a partial CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix=path.stem + "_", suffix=".tmp", dir=path.parent)
    os.close(fd)
    try:
        frame.to_csv(temp_name, index=False)
        os.replace(temp_name, path)
    finally:
        if os.path.exists(temp_name):
            os.remove(temp_name)


def read_csv(path: Path) -> pd.DataFrame:
    initialize_storage()
    try:
        return pd.read_csv(path, dtype={"roll_no": str})
    except pd.errors.EmptyDataError:
        return pd.DataFrame()


def save_student(roll_no, name, branch, academic_year):
    df = read_csv(STUDENTS_FILE)
    row = {"roll_no": str(roll_no), "student_name": name, "branch": branch, "academic_year": academic_year}
    if not df.empty and (df["roll_no"].astype(str) == str(roll_no)).any():
        df.loc[df["roll_no"].astype(str) == str(roll_no), list(row)] = list(row.values())
    else:
        df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    _atomic_csv_write(df, STUDENTS_FILE)


def save_subjects(rows):
    if not rows:
        raise ValueError("No subject rows were supplied.")
    new_df = pd.DataFrame(rows, columns=SUBJECT_COLUMNS)
    if new_df["roll_no"].astype(str).nunique() != 1 or pd.to_numeric(new_df["semester"], errors="coerce").nunique() != 1:
        raise ValueError("A save operation must contain one student and one semester only.")
    df = read_csv(SUBJECTS_FILE)
    roll, sem = str(new_df.iloc[0]["roll_no"]), int(new_df.iloc[0]["semester"])
    if not df.empty:
        df = df[~((df["roll_no"].astype(str) == roll) & (pd.to_numeric(df["semester"], errors="coerce") == sem))]
    _atomic_csv_write(pd.concat([df, new_df], ignore_index=True), SUBJECTS_FILE)


def save_semester(row):
    df = read_csv(SEMESTERS_FILE)
    if not df.empty:
        df = df[~((df["roll_no"].astype(str) == str(row["roll_no"])) & (pd.to_numeric(df["semester"], errors="coerce") == int(row["semester"])))]
    _atomic_csv_write(pd.concat([df, pd.DataFrame([row])], ignore_index=True), SEMESTERS_FILE)


def get_subjects(roll_no=None):
    df = read_csv(SUBJECTS_FILE)
    return df if roll_no is None else df[df["roll_no"].astype(str) == str(roll_no)].copy()


def get_semesters(roll_no=None):
    df = read_csv(SEMESTERS_FILE)
    return df if roll_no is None else df[df["roll_no"].astype(str) == str(roll_no)].copy()


def delete_student(roll_no):
    """Delete one student's profile and associated academic records."""
    for path in (STUDENTS_FILE, SUBJECTS_FILE, SEMESTERS_FILE):
        df = read_csv(path)
        if not df.empty and "roll_no" in df.columns:
            _atomic_csv_write(df[df["roll_no"].astype(str) != str(roll_no)], path)


def _spreadsheet_safe(frame: pd.DataFrame) -> pd.DataFrame:
    """Prefix dangerous text cells to prevent spreadsheet formula execution."""
    safe = frame.copy()
    dangerous = ("=", "+", "-", "@", "\t", "\r")
    for column in safe.select_dtypes(include=["object"]).columns:
        safe[column] = safe[column].map(lambda value: "'" + value if isinstance(value, str) and value.startswith(dangerous) else value)
    return safe


def export_semester(roll_no, semester):
    df = get_subjects(roll_no)
    df = df[pd.to_numeric(df["semester"], errors="coerce") == int(semester)]
    if df.empty:
        raise ValueError("No subject records found for that student and semester.")
    safe_roll = "".join(c for c in str(roll_no) if c.isalnum() or c in "-_")
    if not safe_roll:
        raise ValueError("Roll number cannot be used as an export filename.")
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    path = REPORT_DIR / f"{safe_roll}_semester_{int(semester)}.csv"
    _atomic_csv_write(_spreadsheet_safe(df), path)
    return path