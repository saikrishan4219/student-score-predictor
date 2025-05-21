import pandas as pd
import pickle
from sqlalchemy import create_engine

# Load model and feature columns
with open('student_score_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('feature_columns.pkl', 'rb') as f:
    feature_columns = pickle.load(f)

# Connect to MySQL
engine = create_engine("mysql+pymysql://root:root@localhost/student_db")

# Load data from MySQL
df = pd.read_sql("SELECT * FROM students", con=engine)

# Check if the DataFrame is empty
if df.empty:
    print("⚠️ No data found in 'students' table for prediction.")
else:
    print(f"📊 Data loaded successfully. Number of rows: {len(df)}")

# Preprocessing: One-hot encode categorical columns
categorical_cols = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']
df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# Ensure same columns as training
for col in feature_columns:
    if col not in df_encoded.columns:
        df_encoded[col] = 0  # Adding missing columns with default 0
        print(f"⚠️ Column {col} was missing and added with default 0.")

# Reorder columns to match training data
df_encoded = df_encoded[feature_columns]

# Check if there are any missing values
if df_encoded.isnull().sum().sum() > 0:
    print("⚠️ There are missing values in the data. Please check preprocessing.")

# Make predictions
df['predicted_average_score'] = model.predict(df_encoded)

# Save predictions to new table (replace if already exists)
df[['id', 'predicted_average_score']].to_sql(name='predicted_scores', con=engine, if_exists='replace', index=False)

print("✅ Predictions stored in MySQL.")
