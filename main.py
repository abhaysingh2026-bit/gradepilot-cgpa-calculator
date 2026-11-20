"""ABES Smart CGPA & SGPA Calculator - accessible command-line application."""
import math
from data_manager import (
    initialize_storage, save_student, save_subjects, save_semester,
    get_subjects, get_semesters, delete_student, export_semester
)
from calculator import calculate_sgpa, calculate_cgpa
from grading_system import grade_from_percentage
from analysis import show_subject_results, show_performance

def line():
    print("=" * 66)

def ask_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty.")

def ask_int(prompt, minimum=None, maximum=None):
    while True:
        try:
            value = int(input(prompt).strip())
            if minimum is not None and value < minimum:
                raise ValueError
            if maximum is not None and value > maximum:
                raise ValueError
            return value
        except ValueError:
            print("Enter a valid whole number" +
                  (f" from {minimum} to {maximum}" if maximum is not None else "") + ".")

def ask_float(prompt, minimum=None, maximum=None):
    while True:
        try:
            value = float(input(prompt).strip())
            if not math.isfinite(value):
                raise ValueError
            if minimum is not None and value < minimum:
                raise ValueError
            if maximum is not None and value > maximum:
                raise ValueError
            return value
        except ValueError:
            print("Enter a valid number" +
                  (f" from {minimum} to {maximum}" if maximum is not None else "") + ".")

def register_student():
    line()
    print("STUDENT REGISTRATION")
    roll = ask_text("Roll number: ")
    name = ask_text("Student name: ")
    branch = ask_text("Branch (e.g. CSE AI-ML): ")
    year = ask_text("Academic year (e.g. 2026-27): ")
    save_student(roll, name, branch, year)
    print("Student profile saved successfully.")

def enter_semester_result():
    line()
    print("ENTER SUBJECT DETAILS")
    roll = ask_text("Student roll number: ")
    name = ask_text("Student name: ")
    branch = ask_text("Branch: ")
    year = ask_text("Academic year: ")
    semester = ask_int("Semester (1-8): ", 1, 8)
    count = ask_int("Number of subjects: ", 1, 30)
    rows, credits, grade_points = [], [], []

    for i in range(count):
        print(f"\nSubject {i + 1}")
        code = ask_text("Subject code: ")
        subject = ask_text("Subject name: ")
        course_type = ask_text("Course type (theory/practical/combined/sessional): ").lower()
        if course_type not in {"theory", "practical", "combined", "sessional"}:
            print("Unknown course type. Saved as 'theory'; verify course rules.")
            course_type = "theory"
        credit = ask_float("Credits (greater than 0): ", 0.000001, 100)
        internal_max = ask_float("Maximum internal/sessionals marks: ", 0.000001, 1000)
        internal = ask_float("Internal/sessionals marks obtained: ", 0, internal_max)
        external_max = ask_float("Maximum external/university exam marks (enter 0 if none): ", 0, 1000)
        external = ask_float("External/university exam marks obtained: ", 0, external_max)
        total = internal + external
        maximum = internal_max + external_max
        if maximum <= 0:
            raise ValueError("The combined maximum marks must be greater than zero.")
        percentage = (total / maximum) * 100

        # This project applies only its configurable percentage bands. Subject-wise
        # passing rules vary by ordinance/course type and are intentionally not
        # guessed here. Verify official rules before treating this as a final grade.
        letter, point = grade_from_percentage(percentage)

        print(f"Total: {total:g}/{maximum:g} | {letter} | Grade point: {point}")
        credits.append(credit)
        grade_points.append(point)
        rows.append({
            "roll_no": roll, "student_name": name, "branch": branch,
            "academic_year": year, "semester": semester,
            "subject_code": code, "subject_name": subject, "course_type": course_type,
            "credits": credit, "internal_marks": internal, "internal_max": internal_max,
            "external_marks": external, "external_max": external_max,
            "total_marks": total, "maximum_marks": maximum,
            "percentage": round(percentage, 2), "grade": letter, "grade_point": point
        })

    sgpa = calculate_sgpa(credits, grade_points)
    total_credits = sum(credits)
    save_student(roll, name, branch, year)
    save_subjects(rows)
    save_semester({
        "roll_no": roll, "student_name": name, "branch": branch,
        "academic_year": year, "semester": semester,
        "total_credits": total_credits, "sgpa": round(sgpa, 2)
    })
    print("\nSEMESTER RESULT")
    print(f"Total credits: {total_credits:g}")
    print(f"SGPA: {sgpa:.2f}")
    if any(p == 0 for p in grade_points):
        print("Note: At least one subject received F under the configured percentage bands.")
    print("Reminder: Verify official subject-wise and semester passing rules separately.")

def calculate_overall_cgpa():
    roll = ask_text("Student roll number: ")
    df = get_semesters(roll)
    if df.empty:
        print("No semester records found.")
        return
    sgpas = df["sgpa"].astype(float).tolist()
    credits = df["total_credits"].astype(float).tolist()
    cgpa = calculate_cgpa(sgpas, credits)
    print("\nSEMESTER-WISE RECORD")
    print(df[["semester", "total_credits", "sgpa"]].to_string(index=False))
    print(f"\nOverall CGPA: {cgpa:.2f}")
    print("Percentage conversion is intentionally not displayed; confirm the current")
    print("official ordinance and your college's applicable conversion rule first.")

def view_results():
    roll = ask_text("Student roll number: ")
    show_subject_results(roll)

def performance_analysis():
    roll = ask_text("Student roll number: ")
    show_performance(roll)

def export_results():
    roll = ask_text("Student roll number: ")
    semester = ask_int("Semester (1-8): ", 1, 8)
    try:
        path = export_semester(roll, semester)
        print("Exported successfully to:", path)
    except ValueError as error:
        print(error)

def delete_records():
    roll = ask_text("Enter roll number to delete all its records: ")
    confirm = input(f"Type DELETE to permanently delete records for {roll}: ").strip()
    if confirm == "DELETE":
        delete_student(roll)
        print("Records deleted.")
    else:
        print("Deletion cancelled.")

def main():
    initialize_storage()
    while True:
        line()
        print("       ABES SMART CGPA & SGPA CALCULATOR")
        print("              Python | NumPy | Pandas")
        line()
        print("1. Register / Update Student")
        print("2. Enter Subject Details & Calculate SGPA")
        print("3. Calculate Overall CGPA")
        print("4. View Subject Results")
        print("5. Performance Analysis")
        print("6. Export Semester Result to CSV")
        print("7. Delete Student and All Records")
        print("0. Exit")
        print("Note: Educational estimate only; verify current ABES/AKTU rules.")
        line()
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1": register_student()
            elif choice == "2": enter_semester_result()
            elif choice == "3": calculate_overall_cgpa()
            elif choice == "4": view_results()
            elif choice == "5": performance_analysis()
            elif choice == "6": export_results()
            elif choice == "7": delete_records()
            elif choice == "0":
                print("Thank you for using ABES Smart CGPA Calculator.")
                break
            else: print("Invalid option. Choose from the menu.")
        except (ValueError, KeyError, ZeroDivisionError) as error:
            print("Could not complete this operation:", error)
        input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    main()
