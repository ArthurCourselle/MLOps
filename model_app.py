import streamlit as st
import joblib
import pandas as pd


@st.cache_resource
def load_model():
    return joblib.load("regression.joblib")


model = load_model()

size = st.number_input("Give a size for the house : ")
nb_rooms = st.number_input("Give the number of bedrooms in the house : ")
garden = st.number_input("Is there a garden ?")
if st.button("Predict"):
    df = pd.DataFrame({"size": [size], "nb_rooms": [nb_rooms], "garden": [garden]})
    prediction = model.predict(df)
    st.write(f"Price : {prediction[0]} $")
