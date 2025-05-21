import streamlit as st
import pickle
import pandas as pd
from sqlalchemy import create_engine

# Load model and feature columns
model = pickle.load(open('student_score_model.pkl', 'rb'))
feature_columns = pickle.load(open('feature_columns.pkl', 'rb'))

# MySQL Database connection
engine = create_engine("mysql+pymysql://root:root@localhost/student_db")

# Streamlit UI - Collect user input
st.title("Student Score Prediction")

gender = st.selectbox("Gender", ['female', 'male'])
race = st.selectbox("Race/Ethnicity", ['group A', 'group B', 'group C', 'group D', 'group E'])
parent_edu = st.selectbox("Parental Level of Education", [
    "some high school", "high school", "some college", "associate's degree", "bachelor's degree", "master's degree"
])
lunch = st.selectbox("Lunch", ['standard', 'free/reduced'])
prep = st.selectbox("Test Preparation Course", ['none', 'completed'])

# When user clicks 'Predict'
if st.button("Predict"):
    # Fetch relevant data from MySQL based on user input
    query = f"""
        SELECT * FROM students 
        WHERE gender = '{gender}' 
        AND race_ethnicity = '{race}' 
        AND parental_level_of_education = '{parent_edu}' 
        AND lunch = '{lunch}' 
        AND test_preparation_course = '{prep}'
    """
    df = pd.read_sql(query, con=engine)

    if not df.empty:
        # Preprocessing - One-hot encode categorical features like in the training
        categorical_cols = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']
        df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

        # Ensure same columns as training data
        for col in feature_columns:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
        df_encoded = df_encoded[feature_columns]

        # Perform prediction using the trained model
        predicted_score = model.predict(df_encoded)[0]
        
        st.success(f"Predicted Average Score: {predicted_score:.2f}")

        # Optional: Save predictions back to MySQL
        df['predicted_average_score'] = predicted_score
        df[['id', 'predicted_average_score']].to_sql(name='predicted_scores', con=engine, if_exists='append', index=False)
        st.write("Prediction saved to MySQL.")
        
    else:
        st.error("No matching records found in the database. Please check your input.")
