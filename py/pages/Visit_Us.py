import streamlit as st

# Title with some emoji
st.title("📞 Get in Touch with OutfitX!")

# Attractive Introduction
st.markdown("""
    Have questions or need assistance? We're here to help! Feel free to reach out to us through any of the methods below. 
    Our team is happy to assist you with any inquiries. 💬
""")

# Contact Information Section with Bold Styling
st.markdown("<h3>Contact Information</h3>", unsafe_allow_html=True)

# Email and Phone with Icons and More Styling
st.markdown("""
    📧 **Email**: [support@outfitx.com](mailto:support@outfitx.com)  
    📞 **Phone**: [+123456789](tel:+123456789)  
""", unsafe_allow_html=True)

# Add an additional message to make it more interactive
st.markdown("""
    🕒 **Working Hours**: Monday - Friday, 9 AM - 6 PM (GMT)  
    ⏳ We're here to assist you with any inquiries, and we'll respond as soon as possible!
""")
