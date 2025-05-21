import pandas as pd
from sqlalchemy import create_engine

# 1. Load your CSV
df = pd.read_csv('StudentsPerformance.csv')

# 2. Clean column names to match your MySQL table
df.columns = [
    'gender',
    'race_ethnicity',
    'parental_level_of_education',
    'lunch',
    'test_preparation_course',
    'math_score',
    'reading_score',
    'writing_score'
]

# 3. Connect to MySQL
engine = create_engine("mysql+pymysql://root:root@localhost/student_db")

# 4. Insert data into MySQL (table: students)
df.to_sql(name='students', con=engine, if_exists='append', index=False)

print("✅ Data inserted into MySQL successfully!")
