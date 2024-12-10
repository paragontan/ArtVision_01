import streamlit as st
from PIL import Image
import requests
import base64
import io
pip install --upgrade pip

# OpenAI API Key
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

# OpenAI Vision API endpoint
VISION_API_URL = "https://api.openai.com/v1/images"

# OpenAI GPT API endpoint
GPT_API_URL = "https://api.openai.com/v1/chat/completions"


def identify_art_piece(image):
    """Identify the art piece using OpenAI Vision API."""
    # Convert image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_base64 = base64.b64encode(buffered.getvalue()).decode()

    # Make API request to OpenAI Vision API
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "vision-davinci",
        "image": img_base64,
        "tasks": ["identify"]
    }

    response = requests.post(VISION_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result["output"]["text"]  # Extract identified text
    else:
        st.error("Error identifying the art piece.")
        return None


def generate_description(art_details):
    """Generate a detailed description using OpenAI GPT API."""
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "gpt-4",
        "messages": [
            {
                "role": "system",
                "content": "You are an art expert. Create an accessible description for the visually impaired."
            },
            {
                "role": "user",
                "content": f"Describe this art piece: {art_details}"
            }
        ]
    }

    response = requests.post(GPT_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]  # Extract GPT output
    else:
        st.error("Error generating description.")
        return None


# Streamlit UI
st.title("ArtVision - Accessible Art Descriptions")

# Image Upload
uploaded_image = st.file_uploader("Upload an image of an art piece:", type=["jpg", "jpeg", "png"])

if uploaded_image:
    # Display the uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Art Piece", use_column_width=True)

    # Identify the art piece
    if st.button("Identify and Describe"):
        with st.spinner("Processing..."):
            art_details = identify_art_piece(image)
            if art_details:
                st.subheader("Art Identification")
                st.write(art_details)

                # Generate description
                description = generate_description(art_details)
                if description:
                    st.subheader("Generated Description")
                    st.write(description)
