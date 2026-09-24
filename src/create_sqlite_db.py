from pathlib import Path
import sqlite3


# =================================
# Configuration
# =================================

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# SQLite database path
DATABASE_FILE = PROJECT_ROOT / "data" / "students.db"


# =================================
# Create Database
# =================================

def create_database() -> None:

    # Create the parent folder if it does not exist
    DATABASE_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # Connect to SQLite database
    connection = sqlite3.connect(DATABASE_FILE)

    try:

        cursor = connection.cursor()

        # Create students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                student_id INTEGER,
                name TEXT,
                age INTEGER,
                gpa REAL,
                attendance REAL,
                city TEXT
            )
        """)

        # Save changes
        connection.commit()

        print("SQLite database created successfully")
        print(f"Database path: {DATABASE_FILE.resolve()}")

    finally:

        # Close database connection
        connection.close()


# =================================
# Main
# =================================

if __name__ == "__main__":
    create_database()