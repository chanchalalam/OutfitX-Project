import streamlit as st
from utils import save_uploaded_file

st.title("🔄 Re-Add Item")

re_add_name = st.text_input("Item Name")
re_add_category = st.selectbox("Category", ["Top", "Bottom", "Shoe"])
re_add_season = st.selectbox("Season", ["Spring", "Summer", "Autumn", "Winter"])
re_add_style = st.selectbox("Style", ["Casual", "Formal", "Sport"])
re_add_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

if st.button("✅ Add Item"):
    if not re_add_name or not re_add_style or not re_add_image:
        st.warning("⚠️ Please fill in all fields and upload an image.")
    else:
        file_path = save_uploaded_file(re_add_image)
        if file_path:
            st.success(f"✅ Successfully re-added: {re_add_name} ({re_add_category})")
