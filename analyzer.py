"""NumPy calculations for the Student Marks Analyzer."""
import numpy as np

SUBJECTS = np.array(["Math", "Science", "English", "History", "Computer"])
PASS_MARK = 40


def generate_marks(seed=42):
    """Create reproducible marks for 50 students and five subjects."""
    np.random.seed(seed)
    return np.random.randint(35, 100, (50, 5))


def analyze(marks, pass_mark=PASS_MARK):
    """Return student and subject performance statistics."""
    marks = np.asarray(marks)
    if marks.ndim != 2 or marks.shape[1] != len(SUBJECTS) or marks.shape[0] == 0:
        raise ValueError("Marks must be a nonempty 2D array with five subject columns")
    ids = np.arange(1, marks.shape[0] + 1)
    totals = np.sum(marks, axis=1)
    averages = np.mean(marks, axis=1)
    failures = np.any(marks < pass_mark, axis=1)
    # Grade bands are based on average; F takes priority if any subject is failed.
    grades = np.select(
        [failures, averages >= 90, averages >= 80, averages >= 70, averages >= 60, averages >= 50, averages >= 40],
        ["F", "A+", "A", "B", "C", "D", "E"], default="F"
    )
    return {
        "ids": ids, "totals": totals, "averages": averages,
        "failures": failures, "grades": grades,
        "subject_averages": np.mean(marks, axis=0),
        "subject_pass_percentages": np.mean(marks >= pass_mark, axis=0) * 100,
        "overall_toppers": ids[totals == np.max(totals)],
        "subject_toppers": [ids[marks[:, col] == np.max(marks[:, col])] for col in range(marks.shape[1])],
        "top_ten_indices": np.argsort(-totals, kind="stable")[:10],
    }
