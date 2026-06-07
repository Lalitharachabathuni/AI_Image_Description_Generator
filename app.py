
import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import os

st.title("🖼 AI Image Description & Alt-Text Generator")

api_key = st.text_input("Enter Gemini API Key", type="password")

if api_key:
    genai.configure(api_key=api_key)

    uploaded_files = st.file_uploader(
        "Upload up to 5 Images",
        type=["jpg", "jpeg", "png"],
        accept_multiple_files=True
    )

    if uploaded_files:

        results = []

        model = genai.GenerativeModel("gemini-2.5-flash")

        for file in uploaded_files[:5]:

            image = Image.open(file)

            prompt = """
            Analyze this image and provide:

            1. Brief Alt Text
            2. Detailed Description
            3. SEO Caption
            """

            response = model.generate_content([prompt, image])

            st.image(image, width=300)

            st.subheader(file.name)
            st.write(response.text)

            results.append({
                "Image Name": file.name,
                "Output": response.text
            })

        df = pd.DataFrame(results)

        csv = df.to_csv(index=False)

        st.download_button(
            "Download CSV",
            csv,
            "image_descriptions.csv",
            "text/csv"
        )
