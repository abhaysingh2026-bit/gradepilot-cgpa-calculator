import streamlit as st
import pandas as pd

from calculator import calculate_sgpa, calculate_cgpa
from grading_system import grade_from_percentage


st.set_page_config(
    page_title="ABES Smart CGPA Calculator",
    page_icon="🎓",
    layout="wide"
)

# Initialize session storage
if "semester_records" not in st.session_state:
    st.session_state.semester_records = []

if "last_subjects" not in st.session_state:
    st.session_state.last_subjects = []

if "last_roll" not in st.session_state:
    st.session_state.last_roll = ""


# Header
st.title("🎓 ABES Smart CGPA & SGPA Calculator")
st.subheader("Student Academic Performance Dashboard")

st.write(
    "Calculate SGPA, CGPA, subject grades "
    "and monitor your academic performance."
)

st.info(
    "This calculator provides educational estimates. "
    "Verify official ABES/AKTU grading rules."
)

st.divider()


# Student information
st.header("1. Student Information")

col1, col2 = st.columns(2)

with col1:
    roll_no = st.text_input("Roll Number")
    student_name = st.text_input("Student Name")

with col2:
    branch = st.text_input("Branch", value="CSE AI-ML")
    academic_year = st.text_input(
        "Academic Year", value="2026-27"
    )

semester = st.selectbox(
    "Select Semester",
    list(range(1, 9))
)

st.divider()


# Subject details
st.header("2. Enter Subject Details")

st.write("Enter marks and credits for each subject.")

default_data = pd.DataFrame([
    {
        "subject_code": "",
        "subject_name": "",
        "course_type": "theory",
        "credits": 3.0,
        "internal_marks": 0.0,
        "internal_max": 30.0,
        "external_marks": 0.0,
        "external_max": 70.0
    }
])

subjects_df = st.data_editor(
    default_data,
    num_rows="dynamic",
    use_container_width=True,
    key="subject_editor"
)

st.divider()


# SGPA calculation
st.header("3. Calculate SGPA")

if st.button("Calculate SGPA", type="primary"):

    try:
        if not roll_no.strip():
            raise ValueError("Enter roll number.")

        if not student_name.strip():
            raise ValueError("Enter student name.")

        if not branch.strip() or not academic_year.strip():
            raise ValueError("Enter branch and academic year.")

        credits = []
        grade_points = []
        result_rows = []

        for _, row in subjects_df.iterrows():

            code = str(row["subject_code"]).strip()
            name = str(row["subject_name"]).strip()

            if not code and not name:
                continue

            if not code or not name:
                raise ValueError(
                    "Enter both subject code and subject name."
                )

            credit = float(row["credits"])
            internal = float(row["internal_marks"])
            internal_max = float(row["internal_max"])
            external = float(row["external_marks"])
            external_max = float(row["external_max"])

            values = [
                credit, internal, internal_max,
                external, external_max
            ]

            if not all(pd.notna(v) for v in values):
                raise ValueError("Enter valid numeric values.")

            if credit <= 0:
                raise ValueError("Credits must be greater than zero.")

            if min(internal, internal_max, external, external_max) < 0:
                raise ValueError("Marks cannot be negative.")

            if internal > internal_max:
                raise ValueError(
                    f"Internal marks exceed maximum for {name}."
                )

            if external > external_max:
                raise ValueError(
                    f"External marks exceed maximum for {name}."
                )

            maximum = internal_max + external_max

            if maximum <= 0:
                raise ValueError(
                    f"Maximum marks must be positive for {name}."
                )

            total = internal + external
            percentage = (total / maximum) * 100

            grade, point = grade_from_percentage(percentage)

            credits.append(credit)
            grade_points.append(point)

            result_rows.append({
                "roll_no": roll_no.strip(),
                "student_name": student_name.strip(),
                "branch": branch.strip(),
                "academic_year": academic_year.strip(),
                "semester": semester,
                "subject_code": code,
                "subject_name": name,
                "course_type": row["course_type"],
                "credits": credit,
                "internal_marks": internal,
                "internal_max": internal_max,
                "external_marks": external,
                "external_max": external_max,
                "total_marks": total,
                "maximum_marks": maximum,
                "percentage": round(percentage, 2),
                "grade": grade,
                "grade_point": point
            })

        if not result_rows:
            raise ValueError("Enter at least one subject.")

        sgpa = calculate_sgpa(credits, grade_points)

        total_credits = sum(credits)

        # Update semester record
        records = [
            item for item in st.session_state.semester_records
            if not (
                item["roll_no"] == roll_no.strip()
                and item["semester"] == semester
            )
        ]

        records.append({
            "roll_no": roll_no.strip(),
            "student_name": student_name.strip(),
            "branch": branch.strip(),
            "academic_year": academic_year.strip(),
            "semester": semester,
            "total_credits": total_credits,
            "sgpa": sgpa
        })

        st.session_state.semester_records = records
        st.session_state.last_subjects = result_rows
        st.session_state.last_roll = roll_no.strip()

        st.success("SGPA calculated successfully!")

    except (ValueError, TypeError, KeyError) as error:
        st.error(str(error))


# Display semester result
if (
    st.session_state.last_subjects
    and st.session_state.last_roll == roll_no.strip()
):

    st.divider()
    st.header("4. Semester Result")

    result_df = pd.DataFrame(
        st.session_state.last_subjects
    )

    current_record = next(
        (
            item for item in st.session_state.semester_records
            if item["roll_no"] == roll_no.strip()
            and item["semester"] == semester
        ),
        None
    )

    if current_record:

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "SGPA",
            f"{current_record['sgpa']:.2f}/10"
        )

        col2.metric(
            "Total Credits",
            f"{current_record['total_credits']:g}"
        )

        col3.metric(
            "Total Subjects",
            len(result_df)
        )

        st.subheader("Subject-wise Performance")

        display_columns = [
            "subject_code",
            "subject_name",
            "credits",
            "total_marks",
            "maximum_marks",
            "percentage",
            "grade",
            "grade_point"
        ]

        st.dataframe(
            result_df[display_columns],
            use_container_width=True,
            hide_index=True
        )

        st.download_button(
            "Download Semester Result CSV",
            data=result_df.to_csv(index=False).encode("utf-8"),
            file_name=f"semester_{semester}_result.csv",
            mime="text/csv"
        )


# Overall CGPA
st.divider()
st.header("5. Overall CGPA")

student_records = [
    item for item in st.session_state.semester_records
    if item["roll_no"] == roll_no.strip()
]

if student_records:

    semester_df = pd.DataFrame(student_records)

    semester_df = semester_df.sort_values("semester")

    cgpa = calculate_cgpa(
        semester_df["sgpa"].tolist(),
        semester_df["total_credits"].tolist()
    )

    col1, col2 = st.columns(2)

    col1.metric("Overall CGPA", f"{cgpa:.2f}/10")

    col2.metric(
        "Completed Semesters",
        len(semester_df)
    )

    st.subheader("Semester-wise Performance")

    st.dataframe(
        semester_df,
        use_container_width=True,
        hide_index=True
    )

    st.subheader("SGPA Performance Chart")

    st.bar_chart(
        semester_df.set_index("semester")["sgpa"]
    )

    st.download_button(
        "Download CGPA Report",
        data=semester_df.to_csv(index=False).encode("utf-8"),
        file_name="cgpa_report.csv",
        mime="text/csv"
    )

else:
    st.info(
        "Calculate at least one semester SGPA "
        "to view your overall CGPA."
    )


# Footer
st.divider()

st.caption(
    "ABES Smart CGPA & SGPA Calculator | "
    "Python | NumPy | Pandas | Streamlit"
)

st.caption(
    "Educational estimates only. "
    "Not an official ABES/AKTU result system."
)