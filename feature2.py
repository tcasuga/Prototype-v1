import streamlit as st
import openai

# Set the OpenAI API key directly
openai.api_key = "your api key"

st.title("AI-Powered Water Conservation Tool")

conservation_tip = st.text_input("Enter a water conservation tip or keyword:")

def get_image(prompt):
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        return image_url
    except Exception as e:
        st.error(f"An error occurred while generating the image: {e}")
        return None

if st.button("Generate Water Conservation Image"):
    if conservation_tip:
        prompt = f"Illustration of {conservation_tip} for water conservation"
        image_url = get_image(prompt)  # Call the image generation function
        
        if image_url:
            st.image(image_url, caption=f"Water Conservation: {conservation_tip}")
        else:
            st.write("Could not generate image.")
