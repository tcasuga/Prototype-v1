import os
import openai
import streamlit as st
import pandas as pd
from datetime import datetime

st.markdown("# Water Conservation Tips Generator")
st.sidebar.markdown("# Water Conservation Tips")

openai.api_key = os.environ["OPENAI_API_KEY"]

climate_data = pd.read_csv('city_temperature.csv')

def get_climate_data_from_csv(location):
    today = datetime.now()
    current_month = today.month
    current_day = today.day

    city_data = climate_data[
        (climate_data['City'].str.lower() == location.lower()) &
        (climate_data['Month'] == current_month) &
        (climate_data['Day'] == current_day)
    ]

    if not city_data.empty:
        avg_temp = city_data['AvgTemperature'].values[0]
        print(f"Note: Found data for {location} - Avg Temp: {avg_temp}")
        return f"Average Temperature: {avg_temp}"
    else:
        print("Note: No data found for the given city and date.")
        return "Climate data for the given city and date is not available."

def get_completion(prompt, model="gpt-3.5-turbo"):
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system",
             "content": "Imagine you are helpful assistant that provides and lists 10 personalized water conservation tips based on user inputs. The response should be in a numbered bullet-point format."},
            {"role": "user",
             "content": prompt}
        ]
    )
    return completion.choices[0].message.content

def translate(text, target_language="Spanish"):
    translation_prompt = f"Translate the following text to {target_language}:\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system",
             "content": f"You are a helpful assistant that translates text to {target_language}."},
            {"role": "user",
             "content": translation_prompt}
        ]
    )
    return response.choices[0].message.content

if "tips" not in st.session_state:
    st.session_state.tips = None

if "translated_tips" not in st.session_state:
    st.session_state.translated_tips = None

with st.form(key="water_habits_form"):
    location = st.text_input("Where are you located? (City)")
    household_size = st.number_input("How many people are in the household?", min_value=1, step=1)
    appliances = st.text_input("Appliance usage (e.g., washing machine, dishwasher, water softener, etc.)")
    water_features = st.text_input("Water features (e.g., garden, hot tub, swimming pool, etc.)")
    climate = st.text_input("Describe your climate (e.g., dry, humid, etc.)")
    showering_usage = st.text_input("Describe showering, bathtub, and toilet usage")
    car_wash = st.text_input("How often do you wash your car?")
    
    submitted = st.form_submit_button("Submit")

if submitted:
    climate_data_info = get_climate_data_from_csv(location)
    
    user_inputs = f"""
    Location: {location}
    Household size: {household_size}
    Appliances: {appliances}
    Water features: {water_features}
    Climate: {climate}
    Climate Data: {climate_data_info}
    Showering/bathroom usage: {showering_usage}
    Car wash frequency: {car_wash}
    """
    prompt = f"Based on the following user inputs and climate data, provide personalized water conservation tips:\n{user_inputs}"
    st.session_state.tips = get_completion(prompt)
    st.session_state.translated_tips = None

if st.session_state.tips:
    st.write("Personalized Water Conservation Tips:")
    st.write(st.session_state.tips)

    st.write("### Translate Tips")
    target_language = st.radio("Select Target Language", ["Spanish", "Chinese", "Vietnamese"])

    if st.button("Translate Tips"):
        st.session_state.translated_tips = translate(st.session_state.tips, target_language=target_language)

if st.session_state.translated_tips:
    st.write(f"Translated Water Conservation Tips ({target_language}):")
    st.write(st.session_state.translated_tips)