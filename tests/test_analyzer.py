"""Basic checks for data generation and analysis."""
import numpy as np
from analyzer import SUBJECTS, analyze, generate_marks


def test_subjects():
    assert isinstance(SUBJECTS, np.ndarray)
    assert len(SUBJECTS) == 5


def test_generated_marks_shape_and_range():
    marks = generate_marks()
    assert marks.shape == (50, 5)
    assert np.all((marks >= 35) & (marks < 100))


def test_seed_is_reproducible():
    assert np.array_equal(generate_marks(42), generate_marks(42))


def test_totals_averages_and_failures():
    marks = np.array([[35, 90, 90, 90, 90], [80, 80, 80, 80, 80]])
    results = analyze(marks)
    assert results["totals"].tolist() == [395, 400]
    assert results["averages"].tolist() == [79.0, 80.0]
    assert results["failures"].tolist() == [True, False]
    assert results["grades"].tolist() == ["F", "A"]
    assert results["overall_toppers"].tolist() == [2]
    assert results["subject_pass_percentages"][0] == 50.0


def test_tied_toppers():
    marks = np.array([[90] * 5, [90] * 5])
    results = analyze(marks)
    assert results["overall_toppers"].tolist() == [1, 2]
    assert all(top.tolist() == [1, 2] for top in results["subject_toppers"])


def test_invalid_input():
    import pytest
    with pytest.raises(ValueError):
        analyze(np.array([1, 2, 3]))
