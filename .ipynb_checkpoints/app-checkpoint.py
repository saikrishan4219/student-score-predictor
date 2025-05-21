import streamlit as st
import pickle
import pandas as pd

# Load model and feature columns
model = pickle.load(open('student_score_model.pkl', 'rb'))
feature_columns = pickle.load(open('feature_columns.pkl', 'rb'))

st.title("Student Score Predictor")

# Inputs
gender = st.selectbox("Gender", ['female', 'male'])
race = st.selectbox("Race/Ethnicity", ['group A', 'group B', 'group C', 'group D', 'group E'])
parent_edu = st.selectbox("Parental Level of Education", [
    "some high school", "high school", "some college", "associate's degree", "bachelor's degree", "master's degree"
])
lunch = st.selectbox("Lunch", ['standard', 'free/reduced'])
prep = st.selectbox("Test Preparation Course", ['none', 'completed'])

# Build input dict with one-hot encoding like training
input_dict = {
    'gender_male': 1 if gender == 'male' else 0,
    'race/ethnicity_group B': 1 if race == 'group B' else 0,
    'race/ethnicity_group C': 1 if race == 'group C' else 0,
    'race/ethnicity_group D': 1 if race == 'group D' else 0,
    'race/ethnicity_group E': 1 if race == 'group E' else 0,
    "parental level of education_some high school": 1 if parent_edu == "some high school" else 0,
    "parental level of education_high school": 1 if parent_edu == "high school" else 0,
    "parental level of education_some college": 1 if parent_edu == "some college" else 0,
    "parental level of education_associate's degree": 1 if parent_edu == "associate's degree" else 0,
    "parental level of education_bachelor's degree": 1 if parent_edu == "bachelor's degree" else 0,
    "parental level of education_master's degree": 1 if parent_edu == "master's degree" else 0,
    'lunch_standard': 1 if lunch == 'standard' else 0,
    'test preparation course_completed': 1 if prep == 'completed' else 0,
}

# Create DataFrame with all feature columns and fill missing with 0
input_df = pd.DataFrame([input_dict], columns=feature_columns).fillna(0)

if st.button("Predict"):
    prediction = model.predict(input_df)[0]
    st.success(f"Predicted Average Score: {prediction:.2f}")
