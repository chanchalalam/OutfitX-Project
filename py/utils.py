import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="streamlit")

import streamlit as st
from streamlit_sortables import sort_items
import datetime
import random
import os
from PIL import Image
from recognition_module import single_classification
import uuid
import hashlib
import base64

# --------------------------
# Helper Functions
# --------------------------

def compute_file_hash(uploaded_file):
    """Compute MD5 hash of uploaded file content"""
    return hashlib.md5(uploaded_file.getvalue()).hexdigest()

def get_current_season():
    month = datetime.datetime.now().month
    if 3 <= month <= 5:
        return 'spring'
    elif 6 <= month <= 8:
        return 'summer'
    elif 9 <= month <= 11:
        return 'autumn'
    else:
        return 'winter'

def initialize_session_state():
    if 'tops' not in st.session_state:
        st.session_state.tops = []
    if 'bottoms' not in st.session_state:
        st.session_state.bottoms = []
    if 'shoes' not in st.session_state:
        st.session_state.shoes = []
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'processed_hashes' not in st.session_state:
        st.session_state.processed_hashes = set()
    if 'uploader_key' not in st.session_state:
        st.session_state.uploader_key = 0
    if 'menu_visible' not in st.session_state:
        st.session_state.menu_visible = False

def resize_image(image, target_size=(300, 300)):
    """Resize image to 300x300 pixels while maintaining quality"""
    if image.mode != "RGB":
        image = image.convert("RGB")  # Convert to RGB to avoid format issues
    image = image.resize(target_size, Image.Resampling.LANCZOS)
    return image

def save_uploaded_file(uploaded_file):
    """Save uploaded file after resizing it"""
    try:
        file_path = os.path.join('uploads', uploaded_file.name)
        image = Image.open(uploaded_file)
        image = resize_image(image)  # Resize before saving
        image.save(file_path, format="JPEG", quality=90)  # Save as high-quality JPEG
        return file_path
    except Exception as e:
        st.error(f"Error saving file: {str(e)}")
        return None

