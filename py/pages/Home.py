import streamlit as st

# Set page config with more customization options
st.set_page_config(page_title="OutfitX - Home", layout="wide", initial_sidebar_state="collapsed")

# Center the title and subtitle using custom CSS
st.markdown("""
    <style>
        .title {
            text-align: center;
        }
        .subtitle {
            text-align: center;
            font-size: 24px;
            color: #555;
        }
        .content {
            text-align: center;
            padding-top: 30px;
        }
        .stButton>button {
            display: block;
            margin: 0 auto;
            top: 90px;

        }
        
    </style>
""", unsafe_allow_html=True)

# Title and Subheading with Styling
st.markdown('<h1 class="title">🏠 Welcome to <b>OutfitX</b></h1>', unsafe_allow_html=True)
st.markdown('<h3 class="subtitle">Effortless Fashion, Every Day 👗✨</h3>', unsafe_allow_html=True)

# Add some descriptive text with call-to-action
st.markdown("""
    <div class="content">
        Welcome to OutfitX, the future of fashion at your fingertips! Say goodbye to outfit stress and hello to a world of limitless possibilities. With handpicked styles tailored to you, we create the perfect look in a flash. Ready to redefine your wardrobe? Let’s make every outfit your best one yet!
    </div>
""", unsafe_allow_html=True)

# Add a centered button and text
with st.container():
    # Center the button using the 'stButton>button' class
    button_clicked = st.button('Start Creating Your Outfit')

    # Centered text after the button is clicked
    if button_clicked:
        st.markdown('<p style="text-align:center;">Let\'s start styling! 👚👖👟 </p>', unsafe_allow_html=True)
