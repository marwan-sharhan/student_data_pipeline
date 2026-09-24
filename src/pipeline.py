
from pathlib import Path
import logging
import os
import pandas as pd
import requests
from sqlalchemy import create_engine
import sqlite3
import re


# =================================
# Configuration
# =================================

API_URL = (
    "https://6ab0307fee9c55c910bf96b0.mockapi.io"
    "/api/v1/students"
)

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# File paths
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "students_raw.csv"

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "students_ml_ready.csv"
)

SQLITE_FILE = PROJECT_ROOT / "data" / "students.db"

LOG_FILE = PROJECT_ROOT / "logs" / "pipeline.log"

REQUIRED_COLUMNS = {
    "student_id",
    "name",
    "age",
    "gpa",
    "attendance",
    "city",
}


# PostgreSQL configuration
# سيتم تعديل القيم حسب إعدادات PostgreSQL عندك

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "student_data")

POSTGRES_URL = (
    f"postgresql+psycopg2://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)


# =================================
# Logging
# =================================

LOG_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(message)s"
    )
)

logger = logging.getLogger(__name__)


# =================================
# Common Helpers
# =================================

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    توحيد أسماء الأعمدة وتجهيز البيانات
    القادمة من المصادر المختلفة.
    """

    df = df.copy()

    # حذف المسافات من أسماء الأعمدة
    df.columns = df.columns.str.strip()

    # API قد يحتوي على id إضافي
    # نستخدم student_id باعتباره معرف الطالب
    if "student_id" not in df.columns and "id" in df.columns:
        df = df.rename(columns={"id": "student_id"})

    # حذف عمود id إذا كان زائدًا
    if "id" in df.columns and "student_id" in df.columns:
        df = df.drop(columns=["id"])

    return df


def log_source_result(
    source_name: str,
    df: pd.DataFrame
) -> None:

    logger.info(
        "Source: %s | Rows: %d | Columns: %d",
        source_name,
        len(df),
        len(df.columns)
    )

    print(
        f"{source_name}: "
        f"{len(df)} rows, "
        f"{len(df.columns)} columns"
    )


# =================================
# LOAD 1: CSV
# =================================

def load_data_from_csv(
    file_path: Path
) -> pd.DataFrame:

    logger.info("Loading data from CSV: %s", file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    if df.empty:
        raise ValueError(
            "CSV file is empty"
        )

    df = normalize_columns(df)

    log_source_result("CSV", df)

    return df


# =================================
# LOAD 2: API
# =================================

def load_data_from_api(
    api_url: str
) -> pd.DataFrame:

    logger.info(
        "Loading data from API: %s",
        api_url
    )

    response = requests.get(
        api_url,
        timeout=30
    )

    response.raise_for_status()

    data = response.json()

    if not data:
        raise ValueError(
            "API returned empty data"
        )

    df = pd.DataFrame(data)

    if df.empty:
        raise ValueError(
            "API DataFrame is empty"
        )

    df = normalize_columns(df)

    log_source_result("API", df)

    return df


# =================================
# LOAD 3: SQLite
# =================================

def load_data_from_sqlite(database_file):
    connection = sqlite3.connect(database_file)

    try:
        query = "SELECT * FROM students"
        data = pd.read_sql_query(query, connection)

        print("SQLite data loaded successfully")
        print(f"SQLite rows: {len(data)}")

        return data

    finally:
        connection.close()


# =================================
# LOAD 4: PostgreSQL
# =================================

def load_data_from_postgresql():
    engine = create_engine(POSTGRES_URL)

    try:
        query = "SELECT * FROM students"

        data = pd.read_sql_query(query, engine)

        print("PostgreSQL data loaded successfully")
        print(f"PostgreSQL rows: {len(data)}")

        return data

    finally:
        engine.dispose()

# =================================
# Schema Validation
# =================================

def validate_schema(
    df: pd.DataFrame
) -> None:

    missing_columns = (
        REQUIRED_COLUMNS - set(df.columns)
    )

    if missing_columns:
        raise ValueError(
            "Missing columns: "
            f"{sorted(missing_columns)}"
        )


# =================================
# Type Conversion
# =================================

def convert_data_types(
    df: pd.DataFrame
) -> pd.DataFrame:

    df = df.copy()

    numeric_columns = [
        "student_id",
        "age",
        "gpa",
        "attendance",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    return df


# =================================
# Cleaning
# =================================

def clean_data(data):
    data = data.copy()

    # إزالة الصفوف المتطابقة تمامًا
    data = data.drop_duplicates()

    # إزالة السجلات المكررة حسب رقم الطالب
    if "student_id" in data.columns:
        data = data.drop_duplicates(
            subset=["student_id"]
        )

    # تنظيف النصوص
    text_columns = ["name", "city"]

    for column in text_columns:
        if column in data.columns:
            data[column] = data[column].astype("string").str.strip()

    # التحقق من العمر
    if "age" in data.columns:
        invalid_age = ~data["age"].between(16, 80)
        data.loc[invalid_age, "age"] = pd.NA

    # التحقق من المعدل GPA
    if "gpa" in data.columns:
        invalid_gpa = ~data["gpa"].between(0, 4)
        data.loc[invalid_gpa, "gpa"] = pd.NA

    # التحقق من نسبة الحضور
    if "attendance" in data.columns:
        invalid_attendance = ~data["attendance"].between(0, 100)
        data.loc[invalid_attendance, "attendance"] = pd.NA

    # تعويض القيم المفقودة في الأعمدة الرقمية بالوسيط
    numeric_columns = [
        "age",
        "gpa",
        "attendance"
    ]

    for column in numeric_columns:
        if column in data.columns:
            data[column] = data[column].fillna(
                data[column].median()
            )

    return data

# =================================
# Validation
# =================================

def validate_data(data):
    print("\nStarting data validation...")

    errors = []

    # التحقق من أن الجدول ليس فارغًا
    if data.empty:
        errors.append("The dataset is empty")

    # التحقق من وجود رقم الطالب
    if "student_id" in data.columns:
        if data["student_id"].isna().any():
            errors.append("Missing student_id values")

        if data["student_id"].duplicated().any():
            errors.append("Duplicate student_id values")

    # التحقق من الأسماء
    if "name" in data.columns:
        if data["name"].isna().any():
            errors.append("Missing name values")

    # التحقق من الأعمار
    if "age" in data.columns:
        invalid_age = ~data["age"].between(16, 80)
        if invalid_age.any():
            errors.append("Invalid age values")

    # التحقق من GPA
    if "gpa" in data.columns:
        invalid_gpa = ~data["gpa"].between(0, 4)
        if invalid_gpa.any():
            errors.append("Invalid GPA values")

    # التحقق من نسبة الحضور
    if "attendance" in data.columns:
        invalid_attendance = ~data["attendance"].between(0, 100)
        if invalid_attendance.any():
            errors.append("Invalid attendance values")

    if errors:
        print("Validation failed")

        for error in errors:
            print(f"- {error}")

        return False

    print("Validation passed successfully")
    return True

# =================================
# Save
# =================================

def save_data(data, output_file):
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    data.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig"
    )

    print("\nData saved successfully")
    print(f"Output file: {output_file.resolve()}")
    print(f"Saved rows: {len(data)}")
    print(f"Saved columns: {len(data.columns)}")


# =================================
# Pipeline
# =================================

def run_pipeline() -> None:

    try:

        logger.info(
            "Pipeline started"
        )

        # 1. Read CSV
        csv_df = load_data_from_csv(
            RAW_FILE
        )

        # 2. Read API
        api_df = load_data_from_api(
            API_URL
        )

        # 3. Read SQLite
        sqlite_df = load_data_from_sqlite(
            SQLITE_FILE
        )

        # 4. Read PostgreSQL
        postgres_df = load_data_from_postgresql()

        # 5. Combine all sources
        df = pd.concat(
            [
                csv_df,
                api_df,
                sqlite_df,
                postgres_df
            ],
            ignore_index=True
        )

        print(
            f"Total rows before cleaning: "
            f"{len(df)}"
        )

        logger.info(
            "Combined rows before cleaning: %d",
            len(df)
        )

        # 6. Validate schema
        validate_schema(df)

        # 7. Convert data types
        df = convert_data_types(df)

        # 8. Clean data
        df = clean_data(df)

        # 9. Validate cleaned data
        validate_data(df)

        # 10. Save final data
        save_data(
            df,
            OUTPUT_FILE
        )

        logger.info(
            "Pipeline completed successfully"
        )

        print(
            "Completed successfully"
        )

    except Exception as exc:

        logger.exception(
            "Pipeline failed: %s",
            exc
        )

        print(
            f"Pipeline failed: {exc}"
        )

        raise


def normalize_columns(data):
    data = data.copy()

    # إزالة المسافات من أسماء الأعمدة
    data.columns = data.columns.str.strip()

    # توحيد اسم العمود id إلى student_id
    if "student_id" not in data.columns and "id" in data.columns:
        data = data.rename(columns={"id": "student_id"})

    # إذا كان العمودان موجودين، نحتفظ بـ student_id ونحذف id
    elif "student_id" in data.columns and "id" in data.columns:
        data = data.drop(columns=["id"])

    return data


MIXED_NAMES = [
    "Ahmed",
    "Mohammed",
    "Ali",
    "Sara",
    "Khaled",
    "Fatima",
    "Maryam",
    "Yousef",
    "Noor",
    "Abdullah",
    "Omar",
    "Aisha",
    "Hassan",
    "Mariam",
    "Huda",
    "Mahmoud",
    "Salem",
    "Zainab",
    "Ibrahim",
    "Rania",
    "Mustafa",
    "Amal",
    "Nasser",
    "Layla",
    "Saeed",
    "Reem",
    "Tariq",
    "Mona",
    "Yahya",
    "Samira",
    "Hamza",
    "Lina",
    "Adel",
    "Asma",
    "Faisal",
    "Wafa",
    "Anas",
    "Sana",
    "Marwan",
    "Iman"
]
def assign_mixed_names(data):
    data = data.copy()

    if "name" not in data.columns:
        return data

    name_index = 0

    for index in data.index:
        current_name = str(data.at[index, "name"]).strip()

        # البحث عن الأسماء الوهمية مثل name 1 أو name2
        if re.fullmatch(r"name\s*\d+", current_name, re.IGNORECASE):
            data.at[index, "name"] = MIXED_NAMES[
                name_index % len(MIXED_NAMES)
            ]

            name_index += 1

    return data


# =================================
# Main
# =================================

if __name__ == "__main__":
    print("Starting data pipeline...")

    # قراءة المصادر الأربعة
    sqlite_data = load_data_from_sqlite(SQLITE_FILE)
    csv_data = load_data_from_csv(RAW_FILE)
    api_data = load_data_from_api(API_URL)
    postgres_data = load_data_from_postgresql()

    # دمج البيانات
    all_data = pd.concat(
        [
            sqlite_data,
            csv_data,
            api_data,
            postgres_data
        ],
        ignore_index=True
    )

    print("\nAll data sources merged successfully")
    print(f"Rows before cleaning: {len(all_data)}")

    # توحيد أسماء الأعمدة
    all_data = normalize_columns(all_data)

    #تغيير الاسماء الوهمية فقط

    all_data = assign_mixed_names(all_data)

    # تحويل أنواع البيانات
    all_data = convert_data_types(all_data)

    # تنظيف البيانات
    cleaned_data = clean_data(all_data)

    # التحقق من البيانات بعد التنظيف
    is_valid = validate_data(cleaned_data)

    if not is_valid:
        print("\nPipeline stopped because validation failed")
        raise SystemExit(1)

    # حفظ البيانات النهائية
    save_data(
            cleaned_data,
            OUTPUT_FILE
        )

    print("\nPipeline completed successfully")

    print("\nData is ready for the next stage")

    print("\nData cleaning completed")
    print(f"Rows after cleaning: {len(cleaned_data)}")

    print("\nCleaned data preview:")
    print(cleaned_data.head().to_string(index=False))