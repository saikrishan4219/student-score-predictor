import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle
from sqlalchemy import create_engine

# Load from MySQL instead of CSV
engine = create_engine("mysql+pymysql://root:root@localhost/student_db")
df = pd.read_sql("SELECT * FROM students", con=engine)

print("📡 Data loaded from MySQL:")
print(df.head())

# Create target: average score
df['average_score'] = df[['math_score', 'reading_score', 'writing_score']].mean(axis=1)

# One-hot encode categorical columns
categorical_cols = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']
df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

X = df_encoded.drop(['math_score', 'reading_score', 'writing_score', 'average_score'], axis=1)
y = df_encoded['average_score']

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model and feature columns
with open('student_score_model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('feature_columns.pkl', 'wb') as f:
    pickle.dump(X.columns.tolist(), f)

print("✅ Model trained and saved from MySQL data.")
