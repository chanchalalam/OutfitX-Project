import streamlit as st
import random
from utils import initialize_session_state, get_current_season

st.title("✨ Outfit Recommendation")

initialize_session_state()

if st.button("🔮 Generate Outfit"):
    if not st.session_state.tops or not st.session_state.bottoms or not st.session_state.shoes:
        st.warning("Please add items in all categories first!")
    else:
        top = random.choice(st.session_state.tops)
        bottom = random.choice(st.session_state.bottoms)
        shoe = random.choice(st.session_state.shoes)

        st.subheader("🌟 Today's Perfect Outfit")
        st.markdown(f"👕 **Top:** {top['name']}")
        st.markdown(f"👖 **Bottom:** {bottom['name']}")
        st.markdown(f"👟 **Shoes:** {shoe['name']}")
