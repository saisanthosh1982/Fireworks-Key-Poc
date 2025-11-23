import os
import json
import base64
import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from src.extract import extract_text
from src.parse import parse_fields

load_dotenv()

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

st.set_page_config(page_title="KYC Document Extractor", layout="centered")

st.title("🔍 KYC Identity Document Extractor (Fireworks AI)")
st.write("Upload a Passport or Driver License document to extract identity fields.")


uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])


def save_json(filename, content):
    output_path = os.path.join(OUTPUT_DIR, filename)
    with open(output_path, "w") as f:
        json.dump(content, f, indent=2)
    return output_path


if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Document Preview", width=350)

    file_bytes = uploaded_file.read()

    temp_path = f"samples/_temp_{uploaded_file.name}"
    with open(temp_path, "wb") as f:
        f.write(file_bytes)

    if st.button("🚀 Extract Identity Data"):
        with st.spinner("Extracting text..."):
            raw_text = extract_text(temp_path)

        st.subheader("📄 OCR Extracted Text:")
        st.text_area("Output", raw_text, height=250)

        with st.spinner("Parsing identity fields..."):
            parsed = parse_fields(raw_text)

        try:
            parsed_json = json.loads(parsed)
        except:
            parsed_json = {"error": "Model returned invalid JSON", "raw_response": parsed}

        st.subheader("📦 Structured Identity Output JSON:")
        st.json(parsed_json)

        filename = uploaded_file.name.rsplit(".", 1)[0] + ".json"
        saved_file = save_json(filename, parsed_json)

        st.success(f"Saved structured output to: {saved_file}")
        st.write("You can now process more documents.")

        os.remove(temp_path)
