import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

from calculator import calculate_sgpa, calculate_cgpa
from grading_system import grade_from_percentage


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="GradePilot | CGPA Calculator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# PROFESSIONAL CSS DESIGN
# ==========================================

st.markdown("""
<style>

.stApp {
    background: #f5f7fc;
    color: #172033;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: #172554;
    font-weight: 750;
}

[data-testid="stSidebar"] {
    background: #eef2ff;
}

[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e2e8f0;
    padding: 22px;
    border-radius: 16px;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.05);
}

[data-testid="stMetricValue"] {
    color: #2563eb;
    font-weight: 750;
}

.stButton > button {
    background: #2563eb;
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    font-weight: 650;
}

.stButton > button:hover {
    background: #1d4ed8;
    color: white;
}

.stDownloadButton > button {
    border-radius: 10px;
    border: 1px solid #2563eb;
    color: #2563eb;
    font-weight: 600;
}

div[data-testid="stDataFrame"] {
    border: 1px solid #e2e8f0;
    border-radius: 12px;
}

.hero {
    background: linear-gradient(120deg, #172554, #2563eb);
    padding: 35px;
    border-radius: 20px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 38px;
}

.hero p {
    color: #dbeafe;
    font-size: 16px;
}

.section-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #e2e8f0;
    margin-bottom: 15px;
}

.small-text {
    color: #64748b;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# SESSION STATE
# ==========================================

if "history" not in st.session_state:
    st.session_state.history = []

if "student" not in st.session_state:
    st.session_state.student = {}


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

st.sidebar.title("🎓 GradePilot")
st.sidebar.caption("Your Academic Performance Partner")

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "SGPA Calculator",
        "CGPA Calculator",
        "Semester History",
        "About"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "Calculate your academic performance "
    "and track your progress semester by semester."
)


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def get_grade_details(marks, maximum):
    percentage = (marks / maximum) * 100
    grade, point = grade_from_percentage(percentage)
    return percentage, grade, point


def create_csv_download(data):
    df = pd.DataFrame(data)
    return df.to_csv(index=False).encode("utf-8")


def calculate_grade_label(sgpa):
    if sgpa >= 9:
        return "Excellent"
    elif sgpa >= 8:
        return "Very Good"
    elif sgpa >= 7:
        return "Good"
    elif sgpa >= 6:
        return "Average"
    elif sgpa >= 4:
        return "Pass"
    return "Needs Improvement"


# ==========================================
# DASHBOARD
# ==========================================

if page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>Welcome to GradePilot 🚀</h1>
        <p>Your smart academic performance and CGPA tracking platform.</p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Your Academic Overview")

    history = st.session_state.history

    total_semesters = len(history)

    if total_semesters > 0:
        latest_sgpa = history[-1]["SGPA"]
        overall_cgpa = calculate_cgpa(
            [item["SGPA"] for item in history],
            [item["Total Credits"] for item in history]
        )
        total_credits = sum(
            item["Total Credits"] for item in history
        )
    else:
        latest_sgpa = 0
        overall_cgpa = 0
        total_credits = 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Overall CGPA", f"{overall_cgpa:.2f}")
    col2.metric("Latest SGPA", f"{latest_sgpa:.2f}")
    col3.metric("Semesters", total_semesters)
    col4.metric("Total Credits", total_credits)

    st.divider()

    st.subheader("Quick Actions")

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("### 📘 SGPA Calculator")
        st.write("Calculate your semester grade point average.")
        if st.button("Calculate SGPA", use_container_width=True):
            st.session_state.quick_page = "SGPA Calculator"
            st.rerun()

    with c2:
        st.markdown("### 📊 CGPA Calculator")
        st.write("Calculate your cumulative grade point average.")
        if st.button("Calculate CGPA", use_container_width=True):
            st.session_state.quick_page = "CGPA Calculator"
            st.rerun()

    if history:
        st.divider()
        st.subheader("Your SGPA Progress")

        chart_data = pd.DataFrame({
            "Semester": [item["Semester"] for item in history],
            "SGPA": [item["SGPA"] for item in history]
        })

        st.line_chart(
            chart_data.set_index("Semester"),
            y="SGPA"
        )

    else:
        st.info(
            "You haven't added any semester results yet. "
            "Start by calculating your first SGPA."
        )


# ==========================================
# SGPA CALCULATOR
# ==========================================

elif page == "SGPA Calculator":

    st.title("📘 SGPA Calculator")
    st.caption("Calculate your Semester Grade Point Average.")

    with st.form("student_form"):

        st.subheader("Student Information")

        col1, col2 = st.columns(2)

        with col1:
            student_name = st.text_input(
                "Student Name",
                placeholder="Enter your full name"
            )

            roll_no = st.text_input(
                "Roll Number",
                placeholder="Enter your roll number"
            )

        with col2:
            branch = st.selectbox(
                "Branch",
                [
                    "CSE Core",
                    "CSE AI-ML",
                    "CSE Data Science",
                    "IT",
                    "ECE",
                    "Other"
                ]
            )

            semester = st.selectbox(
                "Semester",
                [f"Semester {i}" for i in range(1, 9)]
            )

        st.divider()

        st.subheader("Subject Details")

        st.write(
            "Enter each subject's credits and marks. "
            "You can add more rows in the table."
        )

        default_subjects = pd.DataFrame({
            "Subject Name": ["Mathematics", "Physics", "Programming"],
            "Credits": [4, 3, 3],
            "Marks Obtained": [80, 75, 85],
            "Maximum Marks": [100, 100, 100]
        })

        subjects = st.data_editor(
            default_subjects,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True,
            column_config={
                "Subject Name": st.column_config.TextColumn(
                    "Subject Name",
                    required=True
                ),
                "Credits": st.column_config.NumberColumn(
                    "Credits",
                    min_value=1,
                    max_value=10,
                    step=1
                ),
                "Marks Obtained": st.column_config.NumberColumn(
                    "Marks Obtained",
                    min_value=0,
                    step=1
                ),
                "Maximum Marks": st.column_config.NumberColumn(
                    "Maximum Marks",
                    min_value=1,
                    step=1
                )
            },
            key="subject_editor"
        )

        submitted = st.form_submit_button(
            "Calculate My SGPA 🚀",
            use_container_width=True
        )

    if submitted:

        if not student_name.strip() or not roll_no.strip():
            st.error("Please enter your name and roll number.")

        elif subjects.empty:
            st.error("Please enter at least one subject.")

        else:
            valid = True
            subject_results = []

            for _, row in subjects.iterrows():

                name = str(row["Subject Name"]).strip()

                if not name:
                    st.error("Subject name cannot be empty.")
                    valid = False
                    break

                if pd.isna(row["Credits"]) or pd.isna(row["Marks Obtained"]) or pd.isna(row["Maximum Marks"]):
                    st.error("Please fill in all subject details.")
                    valid = False
                    break

                credits = float(row["Credits"])
                marks = float(row["Marks Obtained"])
                maximum = float(row["Maximum Marks"])

                if credits <= 0 or maximum <= 0:
                    st.error("Credits and maximum marks must be positive.")
                    valid = False
                    break

                if marks < 0 or marks > maximum:
                    st.error(
                        f"Invalid marks for {name}. "
                        "Marks must be between 0 and maximum marks."
                    )
                    valid = False
                    break

                percentage, grade, point = get_grade_details(
                    marks, maximum
                )

                subject_results.append({
                    "Subject": name,
                    "Credits": credits,
                    "Marks": marks,
                    "Maximum Marks": maximum,
                    "Percentage": round(percentage, 2),
                    "Grade": grade,
                    "Grade Point": point
                })

            if valid and subject_results:

                credits_list = [
                    item["Credits"] for item in subject_results
                ]

                points_list = [
                    item["Grade Point"] for item in subject_results
                ]

                sgpa = calculate_sgpa(
                    credits_list,
                    points_list
                )

                total_credits = sum(credits_list)

                total_marks = sum(
                    item["Marks"] for item in subject_results
                )

                maximum_marks = sum(
                    item["Maximum Marks"] for item in subject_results
                )

                percentage = (
                    total_marks / maximum_marks
                ) * 100

                st.session_state.student = {
                    "Name": student_name,
                    "Roll Number": roll_no,
                    "Branch": branch
                }

                record = {
                    "Student Name": student_name,
                    "Roll Number": roll_no,
                    "Branch": branch,
                    "Semester": semester,
                    "SGPA": round(float(sgpa), 2),
                    "Total Credits": total_credits,
                    "Percentage": round(percentage, 2),
                    "Date": datetime.now().strftime("%d-%m-%Y")
                }

                st.session_state.history.append(record)

                st.success("Your SGPA has been calculated successfully!")

                st.divider()

                st.subheader("🎉 Your Result")

                r1, r2, r3 = st.columns(3)

                r1.metric("Your SGPA", f"{sgpa:.2f}")
                r2.metric("Percentage", f"{percentage:.2f}%")
                r3.metric("Total Credits", total_credits)

                st.markdown(
                    f"### Performance: {calculate_grade_label(sgpa)}"
                )

                st.subheader("Subject-wise Result")

                result_df = pd.DataFrame(subject_results)

                st.dataframe(
                    result_df,
                    use_container_width=True,
                    hide_index=True
                )

                st.download_button(
                    "⬇️ Download Subject Result CSV",
                    data=create_csv_download(subject_results),
                    file_name="gradepilot_subject_result.csv",
                    mime="text/csv"
                )


# ==========================================
# CGPA CALCULATOR
# ==========================================

elif page == "CGPA Calculator":

    st.title("📊 CGPA Calculator")
    st.caption("Calculate your cumulative grade point average.")

    history = st.session_state.history

    if history:

        st.subheader("Your Semester Records")

        history_df = pd.DataFrame(history)

        st.dataframe(
            history_df,
            use_container_width=True,
            hide_index=True
        )

        sgpas = [item["SGPA"] for item in history]
        credits = [item["Total Credits"] for item in history]

        cgpa = calculate_cgpa(sgpas, credits)

        total_credits = sum(credits)

        col1, col2, col3 = st.columns(3)

        col1.metric("Overall CGPA", f"{cgpa:.2f}")
        col2.metric("Completed Semesters", len(history))
        col3.metric("Total Credits", total_credits)

        st.success(
            f"Your current overall CGPA is {cgpa:.2f}"
        )

        st.download_button(
            "⬇️ Download CGPA Report",
            data=create_csv_download(history),
            file_name="gradepilot_cgpa_report.csv",
            mime="text/csv"
        )

    else:
        st.info(
            "No semester records found. "
            "Calculate your SGPA first to see your CGPA."
        )


# ==========================================
# SEMESTER HISTORY
# ==========================================

elif page == "Semester History":

    st.title("📚 Semester History")
    st.caption("Track your academic journey.")

    history = st.session_state.history

    if history:

        df = pd.DataFrame(history)

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Semester Performance")

        chart = df[["Semester", "SGPA"]].copy()

        st.bar_chart(
            chart.set_index("Semester")
        )

        st.download_button(
            "⬇️ Export All Records",
            data=create_csv_download(history),
            file_name="gradepilot_semester_history.csv",
            mime="text/csv"
        )

        if st.button("Clear Session History"):
            st.session_state.history = []
            st.rerun()

    else:
        st.info("Your semester history will appear here.")


# ==========================================
# ABOUT PAGE
# ==========================================

elif page == "About":

    st.title("About GradePilot 🎓")

    st.markdown("""
    <div class="section-card">

    <h2>GradePilot</h2>

    <p>
    GradePilot is a student-focused academic performance
    calculator designed to make SGPA and CGPA calculations
    simple, clear and convenient.
    </p>

    <h3>Key Features</h3>

    <ul>
        <li>Semester Grade Point Average calculation</li>
        <li>Cumulative Grade Point Average calculation</li>
        <li>Subject-wise grade analysis</li>
        <li>Semester performance tracking</li>
        <li>CSV report downloads</li>
        <li>Academic progress visualization</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

    st.caption("GradePilot | Academic Performance Made Simple")


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.markdown(
    """
    <div style="text-align:center; color:#64748b; padding:15px;">
        <b>GradePilot</b> | Academic Performance Made Simple 🎓
        <br>
        <small>Built with Python, Pandas, NumPy and Streamlit</small>
    </div>
    """,
    unsafe_allow_html=True
)