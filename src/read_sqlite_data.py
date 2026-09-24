from pathlib import Path
import sqlite3
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_FILE = PROJECT_ROOT / "data" / "students.db"


def read_sqlite_data() -> None:
    connection = sqlite3.connect(DATABASE_FILE)

    try:
        query = "SELECT * FROM students"

        data = pd.read_sql_query(query, connection)

        print("Data read successfully from SQLite")
        print(f"Number of rows: {len(data)}")
        print("\nStudents data:")
        print(data.to_string(index=False))

    finally:
        connection.close()


if __name__ == "__main__":
    read_sqlite_data()