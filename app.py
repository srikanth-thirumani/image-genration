import streamlit as st
from PIL import Image
import io
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

# Your DreamStudio API key directly in the code
DREAMSTUDIO_API = "add your api key"  # Replace with your API key

# Streamlit app setup
st.title("AI Image Generator")

# Function to generate image using Stability API
def generate_image(text):
    # Initialize the Stability API client
    stability_api = client.StabilityInference(
        key=DREAMSTUDIO_API,  # API key added directly
        verbose=True,
    )

    # Generate image based on the prompt text
    answers = stability_api.generate(
        prompt=text,
        seed=95456,
    )

    # Process the API response and handle the image
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.finish_reason == generation.FILTER:
                st.warning("Your request activated the API's safety filters and could not be processed."
                           " Please modify the prompt and try again.")
                return None
            elif artifact.type == generation.ARTIFACT_IMAGE:
                img = Image.open(io.BytesIO(artifact.binary))
                return img

# Streamlit user input
prompt_text = st.text_input("Enter a prompt to generate an image")

# Button to generate the image
if st.button("Generate Image"):
    if prompt_text:
        with st.spinner("Generating image..."):
            generated_img = generate_image(prompt_text)
            if generated_img:
                st.image(generated_img, caption="Generated Image", use_column_width=True)
    else:
        st.warning("Please enter a prompt to generate an image.")
