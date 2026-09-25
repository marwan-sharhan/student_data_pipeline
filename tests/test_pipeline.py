import pandas as pd

from src.pipeline import clean_data, validate_data


def test_duplicate_student_ids_are_detected():
    data = pd.DataFrame(
        {
            "student_id": [101, 102, 101],
            "name": ["Ahmed", "Mohammed", "Ali"],
            "age": [22, 23, 21],
            "gpa": [3.5, 3.2, 3.8],
            "attendance": [95, 90, 98],
            "city": ["Sanaa", "Aden", "Taiz"],
        }
    )

    result = validate_data(data)

    assert result is False


def test_duplicates_are_not_removed_before_validation():
    data = pd.DataFrame(
        {
            "student_id": [101, 102, 101],
            "name": ["Ahmed", "Mohammed", "Ali"],
            "age": [22, 23, 21],
            "gpa": [3.5, 3.2, 3.8],
            "attendance": [95, 90, 98],
            "city": ["Sanaa", "Aden", "Taiz"],
        }
    )

    cleaned_data = clean_data(data)

    result = validate_data(cleaned_data)

    assert result is False