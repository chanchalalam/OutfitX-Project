import streamlit as st
from utils import compute_file_hash, save_uploaded_file
import os
from PIL import Image

st.title("📤 Upload Clothes")

uploaded_files = st.file_uploader(
    "Upload Your Stylish Pieces",
    type=["png", "jpg", "jpeg"],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        file_hash = compute_file_hash(uploaded_file)

        if file_hash in st.session_state.processed_hashes:
            st.warning(f"⚠️ {uploaded_file.name} already exists")
            continue

        file_path = save_uploaded_file(uploaded_file)
        if file_path:
            st.success(f"Uploaded: {uploaded_file.name}")
