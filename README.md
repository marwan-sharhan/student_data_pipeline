# Student Data Pipeline

## وصف المشروع

مشروع **Student Data Pipeline** هو خط معالجة بيانات (Data Pipeline) مبني باستخدام Python، ويهدف إلى جمع بيانات الطلاب من عدة مصادر مختلفة، ثم دمجها وتنظيفها وتحويلها إلى بيانات منظمة وجاهزة للاستخدام في مراحل التحليل وMachine Learning.

المشروع يطبق عمليًا مفاهيم مهمة في **Data Engineering** مثل:

- التعامل مع الملفات والبيانات الخام
- قراءة البيانات من CSV
- استهلاك REST API
- التعامل مع قواعد البيانات
- دمج البيانات من مصادر متعددة
- تنظيف وتحويل البيانات
- تسجيل عمليات التنفيذ والأخطاء باستخدام Logging
- إنتاج ملف بيانات نهائي جاهز لمرحلة Machine Learning

---

## مصادر البيانات

يعتمد المشروع على عدة مصادر للبيانات:

1. **CSV**
   - قراءة بيانات الطلاب من ملف CSV.

2. **REST API**
   - جلب بيانات الطلاب من API باستخدام مكتبة `requests`.

3. **SQLite**
   - قراءة بيانات الطلاب من قاعدة بيانات SQLite.

4. **PostgreSQL**
   - الاتصال بقاعدة بيانات PostgreSQL وقراءة البيانات منها.

بعد قراءة البيانات من المصادر المختلفة، يتم دمجها في DataFrame واحد ومعالجتها ضمن Pipeline موحدة.

---

## مراحل عمل المشروع

يمر خط معالجة البيانات بالمراحل الرئيسية التالية:

```text
CSV
      REST API ----              SQLite ------- > Data Integration
              /
PostgreSQL --/

        ↓

Data Cleaning

        ↓

Data Transformation

        ↓

Processed Data

        ↓

students_ml_ready.csv

        ↓

Machine Learning
```

---

## التقنيات والمكتبات المستخدمة

### Python

لغة البرمجة الأساسية المستخدمة في المشروع.

### Pandas

تستخدم لقراءة البيانات ومعالجتها ودمجها وتنظيفها وتحويلها.

### Requests

تستخدم للاتصال بـ REST API وجلب البيانات.

### SQLAlchemy

تستخدم لإنشاء وإدارة الاتصال بقواعد البيانات من خلال Python.

### psycopg2-binary

تستخدم كـ PostgreSQL driver للاتصال بقاعدة بيانات PostgreSQL عند استخدام SQLAlchemy.

### SQLite3

مكتبة مدمجة مع Python للتعامل مع SQLite، ولا تحتاج إلى تثبيت منفصل باستخدام pip.

### re

مكتبة Regular Expressions المدمجة مع Python وتستخدم لمعالجة النصوص والتحقق من الأنماط، ولا تحتاج إلى تثبيت منفصل.

### Logging

تستخدم لتسجيل عمليات تشغيل الـ Pipeline والأخطاء والمعلومات المهمة.

---

## متطلبات التشغيل

يحتاج المشروع إلى:

- Python 3.x
- PostgreSQL
- اتصال بالإنترنت للوصول إلى REST API
- المكتبات الموجودة في `requirements.txt`

---

## تثبيت المشروع

### 1. استنساخ المشروع

```bash
git clone <repository-url>
```

### 2. الدخول إلى مجلد المشروع

```bash
cd student_data_pipeline
```

### 3. إنشاء Virtual Environment

على Windows:

```bash
python -m venv .venv
```

### 4. تفعيل البيئة الافتراضية

في Windows:

```bash
.venv\Scripts\activate
```

### 5. تثبيت المكتبات

```bash
pip install -r requirements.txt
```

---

## إعداد PostgreSQL

يجب إنشاء قاعدة بيانات PostgreSQL وتجهيز بيانات الاتصال الخاصة بها قبل تشغيل الأجزاء التي تعتمد على PostgreSQL.

يجب عدم وضع كلمات المرور أو بيانات الاتصال السرية مباشرة داخل GitHub.

يفضل استخدام متغيرات البيئة (Environment Variables) عند التعامل مع بيانات الاعتماد.

---

## تشغيل المشروع

الملف الرئيسي لمعالجة البيانات هو:

```text
src/pipeline.py
```

لتشغيل الـ Pipeline:

```bash
python src/pipeline.py
```

يقوم البرنامج بقراءة البيانات من المصادر المحددة، ثم دمجها ومعالجتها وتنظيفها وإنتاج البيانات النهائية.

---

## مخرجات المشروع

من أهم المخرجات:

```text
data/processed/students_ml_ready.csv
```

وهو ملف البيانات المعالجة والجاهزة للانتقال إلى مرحلة Machine Learning.

كما يحتوي المشروع على ملفات البيانات الخام وقاعدة SQLite وملفات Logging حسب إعداد المشروع.

---

## هيكل المشروع

```text
student_data_pipeline/
│
├── .gitignore
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/
│   │   └── students_raw.csv
│   │
│   ├── processed/
│   │   └── students_ml_ready.csv
│   │
│   └── students.db
│
├── logs/
    ├── pipeline.log
│
└── src/
    ├── create_sqlite_db.py
    ├── insert_sqlite_data.py
    ├── read_sqlite_data.py
    └── pipeline.py
```

---

## وصف ملفات المشروع

### `src/pipeline.py`

الملف الرئيسي للـ Pipeline.

مسؤول عن تنفيذ مراحل تحميل البيانات من المصادر المختلفة، دمجها، تنظيفها وتحويلها وإنتاج البيانات النهائية.

### `src/create_sqlite_db.py`

يستخدم لإنشاء قاعدة بيانات SQLite.

### `src/insert_sqlite_data.py`

يستخدم لإدخال البيانات إلى قاعدة SQLite.

### `src/read_sqlite_data.py`

يستخدم لقراءة البيانات من SQLite.

### `data/raw/`

يحتوي على البيانات الخام قبل المعالجة.

### `data/processed/`

يحتوي على البيانات بعد المعالجة والتنظيف.

### `logs/`

يحتوي على ملفات سجل التشغيل والأخطاء والمعلومات المتعلقة بالـ Pipeline.

### `requirements.txt`

يحتوي على مكتبات Python الخارجية المطلوبة لتشغيل المشروع.

### `.gitignore`

يحدد الملفات والمجلدات التي يجب ألا يقوم Git بتتبعها أو رفعها إلى GitHub، مثل البيئة الافتراضية والملفات المؤقتة.

---

## Data Cleaning

بعد جمع البيانات من المصادر المختلفة، يتم تنفيذ عمليات تنظيف ومعالجة للبيانات بهدف جعلها أكثر اتساقًا وقابلية للاستخدام.

يمكن أن تشمل عمليات التنظيف:

- معالجة القيم المفقودة
- إزالة أو معالجة السجلات غير الصحيحة
- توحيد أنواع البيانات
- تنظيف النصوص
- التحقق من القيم
- إزالة التكرارات عند الحاجة
- تجهيز الأعمدة للاستخدام في Machine Learning

---

## Data Integration

الميزة الأساسية في المشروع هي القدرة على جمع البيانات من أكثر من مصدر ودمجها في Pipeline واحدة.

بدل التعامل مع كل مصدر بشكل منفصل، يتم تحويل البيانات إلى شكل موحد ثم دمجها في مجموعة بيانات واحدة.

مثال:

```text
CSV
API
SQLite
PostgreSQL
   ↓
DataFrames
   ↓
Merge / Concatenation
   ↓
Cleaning
   ↓
Transformation
   ↓
ML-Ready Dataset
```

---

## Machine Learning Preparation

بعد انتهاء مرحلة Data Cleaning وData Transformation، يتم إنتاج:

```text
students_ml_ready.csv
```

هذا الملف يمثل نقطة انتقال من مرحلة **Data Engineering** إلى مرحلة **Machine Learning**.

قبل بناء نموذج Machine Learning، يمكن تنفيذ مراحل إضافية مثل:

1. تحليل البيانات (EDA)
2. تحديد Target
3. اختيار Features
4. تحويل البيانات النصية إلى قيم رقمية عند الحاجة
5. تقسيم البيانات إلى Training وTesting
6. تدريب نموذج Machine Learning
7. تقييم النموذج

---

## Logging

يستخدم المشروع نظام Logging لتسجيل الأحداث المهمة أثناء تشغيل الـ Pipeline.

يمكن أن تتضمن السجلات:

- بداية تشغيل Pipeline
- مصدر البيانات الذي تتم قراءته
- عدد الصفوف المستخرجة
- الأخطاء
- نجاح مراحل المعالجة
- نهاية عملية التنفيذ

يساعد Logging على اكتشاف الأخطاء ومتابعة مراحل تنفيذ المشروع.

---

## Git وGitHub

يستخدم المشروع Git لإدارة الإصدارات والتغييرات، ويمكن رفعه إلى GitHub لمشاركة المشروع وحفظ نسخه.

مثال على أول Commit:

```bash
git add .
git commit -m "Initial commit: complete student data pipeline"
```

---

## الهدف التعليمي

تم تصميم المشروع لتطبيق مجموعة من مفاهيم Data Engineering بشكل عملي، بداية من استخراج البيانات من مصادر متعددة، مرورًا بعملية الدمج والتنظيف والتحويل، وصولًا إلى إنتاج Dataset يمكن استخدامها في Machine Learning.

---

## التطوير المستقبلي

يمكن تطوير المشروع مستقبلًا بإضافة:

- المزيد من مصادر البيانات
- Data Validation أكثر تقدمًا
- معالجة أفضل للأخطاء
- Automated Testing
- Docker
- CI/CD
- Data Quality Checks
- Machine Learning Pipeline
- Model Training
- Model Evaluation
- MLOps

---


