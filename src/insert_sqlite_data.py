from pathlib import Path
import sqlite3


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_FILE = PROJECT_ROOT / "data" / "students.db"


def insert_sample_data() -> None:
    connection = sqlite3.connect(DATABASE_FILE)

    try:
        cursor = connection.cursor()

        sample_students = [
            (101, "Ahmed", 22, 3.5, 95, "Sana'a"),
            (102, "Mohammed", 24, 3.2, 88, "Aden"),
            (103, "Ali", 21, 3.8, 97, "Taiz"),
            (104, "Sara", 23, 3.9, 92, "Ibb"),
            (105, "Mona", 25, 2.9, 80, "Hodeidah")
        ]

        cursor.executemany(
            """
            INSERT INTO students
            (student_id, name, age, gpa, attendance, city)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            sample_students
        )

        connection.commit()

        print("Sample data inserted successfully")
        print(f"Number of inserted students: {len(sample_students)}")

    finally:
        connection.close()


if __name__ == "__main__":
    insert_sample_data()