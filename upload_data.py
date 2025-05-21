import pandas as pd
from sqlalchemy import create_engine

# 🧠 Replace these values with your FreeSQLDatabase credentials
HOST = "sql12.freesqldatabase.com"
PORT = 3306
USER = "sql12780298"
PASSWORD = "jyJD7RaKFq"
DATABASE = "sql12780298"

# Create the connection URL
engine = create_engine(f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}")

# Load your CSV
df = pd.read_csv("StudentsPerformance.csv")  # Make sure this file is in the same folder

# Push data to MySQL
df.to_sql("student_scores", con=engine, if_exists="replace", index=False)

print("✅ Data uploaded successfully.")
