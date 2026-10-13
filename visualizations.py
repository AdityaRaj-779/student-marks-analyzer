"""Save charts without mixing plotting with NumPy calculations."""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")  # Works in terminals without a graphical display.
import matplotlib.pyplot as plt
import numpy as np
from analyzer import SUBJECTS


def save_charts(results, output_dir="output"):
    folder = Path(output_dir)
    folder.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(SUBJECTS, results["subject_averages"])
    ax.set(title="Subject-wise Average Marks", ylabel="Average marks", ylim=(0, 100))
    fig.tight_layout()
    fig.savefig(folder / "subject_averages.png")
    plt.close(fig)

    labels = ["A+", "A", "B", "C", "D", "E", "F"]
    counts = [np.count_nonzero(results["grades"] == grade) for grade in labels]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(labels, counts)
    ax.set(title="Student Grade Distribution", xlabel="Grade", ylabel="Number of students")
    fig.tight_layout()
    fig.savefig(folder / "grade_distribution.png")
    plt.close(fig)
