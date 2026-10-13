"""Run the Student Marks Analyzer from the command line."""
import csv
from pathlib import Path
import numpy as np
from analyzer import SUBJECTS, PASS_MARK, analyze, generate_marks
from visualizations import save_charts


def export_csv(marks, results, output_dir="output"):
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / "student_results.csv"
    with target.open("w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Student ID", *SUBJECTS.tolist(), "Total", "Average", "Grade", "Status"])
        for index, row in enumerate(marks):
            writer.writerow([int(results["ids"][index]), *row.tolist(), int(results["totals"][index]),
                             f"{results['averages'][index]:.2f}", results["grades"][index],
                             "Fail" if results["failures"][index] else "Pass"])
    return target


def main():
    marks = generate_marks()
    results = analyze(marks)
    print("\n=== STUDENT MARKS ANALYZER ===")
    print("Subjects:", SUBJECTS)
    print(f"Shape: {marks.shape} | ndim: {marks.ndim} | size: {marks.size} | dtype: {marks.dtype}")
    print("\nFirst student, first subject:", marks[0, 0])
    print("Last student, last subject (negative indexing):", marks[-1, -1])
    print("\nFirst 10 students (2D slicing):\n", marks[:10, :])
    print("\nLast subject (all students):\n", marks[:, -1])
    print("\nFirst five students, subjects 2 through 4:\n", marks[:5, 1:4])
    print("\nMarks below 40 (Boolean masking):", marks[marks < 40])
    print("Marks above 90 (Boolean masking):", marks[marks > 90])
    print("\nStudent totals:", results["totals"])
    print("Student averages:", np.round(results["averages"], 2))
    print("\nOverall topper ID(s):", results["overall_toppers"].tolist())
    for i, subject in enumerate(SUBJECTS):
        print(f"{subject}: average {results['subject_averages'][i]:.2f}, "
              f"pass {results['subject_pass_percentages'][i]:.1f}%, "
              f"topper ID(s) {results['subject_toppers'][i].tolist()}")
    print(f"\nStudents failing any subject (mark < {PASS_MARK}):", results["ids"][results["failures"]].tolist())
    print("\nGrade distribution:")
    for grade in ["A+", "A", "B", "C", "D", "E", "F"]:
        print(f"  {grade}: {np.count_nonzero(results['grades'] == grade)}")
    print("\nTOP 10 STUDENTS")
    print("Rank | ID | Total | Average | Grade")
    for rank, index in enumerate(results["top_ten_indices"], 1):
        print(f"{rank:>4} | {results['ids'][index]:>2} | {results['totals'][index]:>5} | "
              f"{results['averages'][index]:>7.2f} | {results['grades'][index]}")
    csv_path = export_csv(marks, results)
    save_charts(results)
    print(f"\nCSV saved: {csv_path}")
    print("Charts saved: output/subject_averages.png and output/grade_distribution.png")


if __name__ == "__main__":
    main()
