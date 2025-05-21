import pandas as pd
from sqlalchemy import create_engine

# MySQL connection setup
engine = create_engine("mysql+pymysql://root:root@localhost/student_db")

# Fetch data from MySQL
df = pd.read_sql("SELECT * FROM students", con=engine)

# Optional: Save to CSV if needed
df.to_csv("fetched_students.csv", index=False)

print("Data fetched successfully from MySQL:")
print(df.head())
