import os
import openai
import streamlit as st

st.markdown("# Water Conservation Tips Generator")
st.sidebar.markdown("# Water Conservation Tips")

openai.api_key = os.environ["OPENAI_API_KEY"]

def get_completion(prompt, model="gpt-3.5-turbo"):
    completion = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system",
             "content": "You are a helpful assistant that provides personalized water conservation tips based on user inputs."},
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
    location = st.text_input("Where are you located?")
    household_size = st.number_input("How many people are in the household?", min_value=1, step=1)
    appliances = st.text_input("Appliance usage (e.g., washing machine, dishwasher, water softener, etc.)")
    water_features = st.text_input("Water features (e.g., garden, hot tub, swimming pool, etc.)")
    climate = st.text_input("Describe your climate (e.g., dry, humid, etc.)")
    showering_usage = st.text_input("Describe showering, bathtub, and toilet usage")
    car_wash = st.text_input("How often do you wash your car?")
    
    submitted = st.form_submit_button("Submit")

if submitted:
    user_inputs = f"""
    Location: {location}
    Household size: {household_size}
    Appliances: {appliances}
    Water features: {water_features}
    Climate: {climate}
    Showering/bathroom usage: {showering_usage}
    Car wash frequency: {car_wash}
    """
    prompt = f"Based on the following user inputs, provide personalized water conservation tips:\n{user_inputs}"
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
