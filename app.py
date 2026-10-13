"""Interactive Streamlit dashboard for the Student Marks Analyzer."""
import csv
from io import StringIO

import numpy as np
import streamlit as st

from analyzer import PASS_MARK, SUBJECTS, analyze, generate_marks


GRADE_ORDER = ["A+", "A", "B", "C", "D", "E", "F"]


def build_student_rows(marks, results):
    """Combine original marks and analyzer results into display-ready rows."""
    rows = []
    for index, subject_marks in enumerate(marks):
        rows.append(
            {
                "Student ID": int(results["ids"][index]),
                **{
                    subject: int(subject_marks[column])
                    for column, subject in enumerate(SUBJECTS.tolist())
                },
                "Total": int(results["totals"][index]),
                "Average": round(float(results["averages"][index]), 2),
                "Grade": str(results["grades"][index]),
                "Status": "Fail" if results["failures"][index] else "Pass",
            }
        )
    return rows


def make_csv(rows, columns):
    """Serialize rows in memory so dashboard downloads never overwrite output."""
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=columns)
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue().encode("utf-8")


st.set_page_config(
    page_title="Student Marks Analyzer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .block-container { max-width: 1440px; padding-top: 2rem; }
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #dce5e0;
        border-radius: 6px;
        padding: 14px 16px;
    }
    [data-testid="stMetricLabel"] { color: #53645c; }
    [data-testid="stMetricValue"] { color: #163d30; }
    div.stButton > button, div.stDownloadButton > button {
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

marks = generate_marks()
analysis = analyze(marks)
student_rows = build_student_rows(marks, analysis)
all_columns = ["Student ID", *SUBJECTS.tolist(), "Total", "Average", "Grade", "Status"]

st.title("Student Marks Analyzer")
st.caption("Class performance overview · 50 students · 5 subjects · NumPy analysis")

with st.sidebar:
    st.header("Explore results")
    student_search = st.text_input("Search student ID", placeholder="For example, 12")
    selected_grades = st.multiselect("Filter by grade", GRADE_ORDER, default=GRADE_ORDER)
    selected_subject = st.selectbox("Subject analysis", SUBJECTS.tolist())
    st.caption(f"Pass threshold: {PASS_MARK} marks in every subject")

passed_count = int(np.count_nonzero(~analysis["failures"]))
failed_count = int(np.count_nonzero(analysis["failures"]))
topper_ids = ", ".join(str(int(student_id)) for student_id in analysis["overall_toppers"])
class_average = float(np.mean(analysis["averages"]))

metric_columns = st.columns(5)
metric_columns[0].metric("Total students", len(student_rows))
metric_columns[1].metric("Passed", passed_count)
metric_columns[2].metric("Failed", failed_count)
metric_columns[3].metric("Overall topper", f"ID {topper_ids}")
metric_columns[4].metric("Class average", f"{class_average:.2f} / 100")

st.divider()
left_chart, right_chart = st.columns(2)

with left_chart:
    st.subheader("Subject-wise average marks")
    st.bar_chart(
        {
            "Subject": SUBJECTS.tolist(),
            "Average marks": analysis["subject_averages"].round(2).tolist(),
        },
        x="Subject",
        y="Average marks",
        y_label="Average marks",
        height=300,
    )

with right_chart:
    st.subheader("Grade distribution")
    grade_rows = [
        {"Grade": grade, "Students": int(np.count_nonzero(analysis["grades"] == grade))}
        for grade in GRADE_ORDER
    ]
    st.bar_chart(grade_rows, x="Grade", y="Students", y_label="Students", height=300)

distribution_column, top_column = st.columns(2)
with distribution_column:
    st.subheader("Pass vs. fail")
    st.bar_chart(
        [{"Status": "Pass", "Students": passed_count}, {"Status": "Fail", "Students": failed_count}],
        x="Status",
        y="Students",
        y_label="Students",
        height=300,
    )

with top_column:
    st.subheader("Top 10 students")
    top_rows = [
        {
            "Student": f"ID {int(analysis['ids'][index])}",
            "Total marks": int(analysis["totals"][index]),
        }
        for index in analysis["top_ten_indices"]
    ]
    st.bar_chart(top_rows, x="Student", y="Total marks", y_label="Total marks", height=300)

st.divider()
st.subheader("Subject performance comparison")
subject_index = SUBJECTS.tolist().index(selected_subject)
subject_metrics = st.columns(3)
subject_metrics[0].metric("Selected subject", selected_subject)
subject_metrics[1].metric("Class average", f"{analysis['subject_averages'][subject_index]:.2f}")
subject_metrics[2].metric(
    "Students passing",
    f"{analysis['subject_pass_percentages'][subject_index]:.1f}%",
)
st.caption(f"Marks distribution for {selected_subject}")
bin_edges = np.arange(30, 111, 10)
bin_counts, _ = np.histogram(marks[:, subject_index], bins=bin_edges)
histogram_rows = [
    {"Marks": f"{lower}-{upper - 1}", "Students": int(count)}
    for lower, upper, count in zip(bin_edges[:-1], bin_edges[1:], bin_counts)
]
st.bar_chart(histogram_rows, x="Marks", y="Students", y_label="Students", height=260)

st.divider()
st.subheader("Student results")
filtered_rows = [
    row
    for row in student_rows
    if row["Grade"] in selected_grades
    and (not student_search or student_search.strip() in str(row["Student ID"]))
]
st.caption(f"Showing {len(filtered_rows)} of {len(student_rows)} students")
st.dataframe(filtered_rows, hide_index=True)
st.download_button(
    "Download visible results as CSV",
    data=make_csv(filtered_rows, all_columns),
    file_name="student_results.csv",
    mime="text/csv",
    disabled=not filtered_rows,
)