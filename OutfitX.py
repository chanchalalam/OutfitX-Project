import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="streamlit")

import streamlit as st
import datetime
import random
import os
from PIL import Image
# from recognition_module import single_classification
import uuid
import hashlib
import base64
import numpy as np
import cv2

def single_classification(single_path):
    
    """
    This function take a single path of a photo, then do reshape to fit the models, and do classification
    Input is a path of a certain photo
    Output is a tuple which contains subtype(for being send to a correct sub-model), 
                                     info(a string having all info of a clothes), 
                                     res(a list having all info of a clothes)
    """
    
    # Our model only applies to dataframes. 
    # Therefore, in order to enable the model to predict a single picture, 
    # we turn this picture into a dataframe with only one row.
    train_images = np.zeros((1,80,60,3))
  
    path = single_path#/content/images   
    img = cv2.imread(path)
    
    #reshape img to apply the model
    if img.shape != (80,60,3):
        img = image.load_img(path, target_size=(80,60,3))

    train_images[0] = img

    
    result2 = sub_list[np.argmax(sub_model.predict(train_images))]
    
    # According to the results of the first model, branch to three other models
    if result2=="top":
        res = single_helper(train_images,top_model,top_list)
    elif result2=="bottom":
        res = single_helper(train_images,bottom_model,bottom_list)
    elif result2=="foot":
        res = single_helper(train_images,foot_model,foot_list)
    res.append(single_path)
    res_str = f"{res[0]}, {res[1]}, {color_classification(single_path)}, {res[3]}, {res[4]}, {single_path}" 
    
    return (result2,res_str,res)

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


def display_category(items, category_name):
    """Displays clothing items with a hover button for details"""
    if not items:
        st.info(f"No {category_name} available. Upload items using the sidebar!")
        return

    for idx, item in enumerate(items):
        cols = st.columns([1, 4])

        with cols[0]:
            try:
                st.image(item['thumbnail'], use_container_width=True)
            except Exception as e:
                st.error(f"Error loading thumbnail: {str(e)}")

        with cols[1]:
            with st.expander("🔍 Item Details"):
                st.markdown(f"**{item['name']}**")
                st.markdown(f"- **Category:** {category_name.title()}")
                st.markdown(f"- **Season:** {item['season'].title()}")
                st.markdown(f"- **Style:** {item['style'].title()}")

                if st.button(f"🗑 Delete {item['name']}", key=f"del_{category_name}_{idx}"):
                    st.session_state[category_name].pop(idx)
                    st.session_state.processed_hashes = {i['file_hash'] for i in 
                                                         st.session_state.tops + 
                                                         st.session_state.bottoms + 
                                                         st.session_state.shoes}
                    st.rerun()


# --------------------------
# Main Application
# --------------------------

def main():
    st.set_page_config(page_title="OutfitX", layout="wide")

    initialize_session_state()
    st.markdown("""
    <style>
        /* Hide the sidebar items by targeting their specific CSS selectors */
        [data-testid="stSidebarNav"] ul li:nth-child(1), /* Config */
        [data-testid="stSidebarNav"] ul li:nth-child(2), /* Contact Us */
        [data-testid="stSidebarNav"] ul li:nth-child(3), /* Home */
        [data-testid="stSidebarNav"] ul li:nth-child(4), /* My Closets */
        [data-testid="stSidebarNav"] ul li:nth-child(5), /* ReAdd Item */
        [data-testid="stSidebarNav"] ul li:nth-child(6), /* Recommendation */
        [data-testid="stSidebarNav"] ul li:nth-child(7), /* Upload Clothes */
        [data-testid="stSidebarNav"] ul li:nth-child(8)  /* Add more if necessary */
        {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)
    st.markdown("""
    <style>
        /* Hide sidebar and remove its space */
        [data-testid="stSidebarNav"] {
            display: none;
        }
        section[data-testid="stSidebarContent"] {
            padding: 0 !important;
            margin: 0 !important;
        }
        .main .block-container {
            padding-top: 1rem !important;
        }
    </style>
""", unsafe_allow_html=True)


    menu_html = """
    <style>
        .menu-container {
            position: absolute;
            top: 70px;
            right: 20px;
            z-index: 1000;
        }
        .menu-btn {
            font-size: 24px;
            cursor: pointer;
            background: none;
            border: none;
            color: white;
        }
        .menu-dropdown {
            display: none;
            position: absolute;
            right: 0;
            background-color: black;
            box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
            border-radius: 5px;
            width: 200px;
            z-index: 1001;
        }
        .menu-dropdown a {
            display: block;
            padding: 10px;
            text-decoration: none;
            color: white;
            font-size: 16px;
        }
        .menu-dropdown a:hover {
            background-color: #444;
        }
        .menu-container:hover .menu-dropdown {
            display: block;
        }
        .logo {
            width: 150px;
        }
    </style>
    <div class="menu-container">
    <button class="menu-btn">☰</button>
        <div class="menu-dropdown">
            <a href="/Home" target="_self">🏠 Home</a>
            <a href="/Upload_Clothes" target="_self">📤 Upload Clothes</a>
            <a href="/My_Closets" target="_self">👚 My Closet</a>
            <a href="/ReAdd_Item" target="_self">🔄 Re-Add Item</a>
            <a href="/Recommendation" target="_self">✨ Recommendation</a>
            <a href="/Visit_Us" target="_self">📞 Visit Us</a>
        </div>
    </div>
    """
    st.markdown(menu_html, unsafe_allow_html=True)
    # Display Logo
    logo_path = "logo1.png"
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode()
        st.markdown(f'<img src="data:image/png;base64,{img_base64}" class="logo">', unsafe_allow_html=True)

    st.title("OutfitX - Effortless Fashion, Every Day 👗✨")
    st.markdown("---")

    # --------------------------
    # Sidebar - File Upload
    # --------------------------

    with st.sidebar:
    
        st.header("📤✨ Add to Your Closet!")
        uploaded_files = st.file_uploader(
            "📸 Upload Your Stylish Pieces",
            type=["png", "jpg", "jpeg", "bmp", "gif"],
            accept_multiple_files=True,
            key=f"file_uploader_{st.session_state.uploader_key}"
        )

        if uploaded_files:
            new_hashes = set()
            for uploaded_file in uploaded_files:
                file_hash = compute_file_hash(uploaded_file)

                if file_hash in st.session_state.processed_hashes:
                    st.warning(f"⚠️ {uploaded_file.name} already exists")
                    continue

                file_path = save_uploaded_file(uploaded_file)
                if file_path:
                    try:
                        sub, info, res_place_holder = single_classification(file_path)
                        item = {
                            "id": str(uuid.uuid4()),
                            "name": info,
                            "season": res_place_holder[3],
                            "style": res_place_holder[4],
                            "thumbnail": Image.open(file_path).resize((100, 100)),
                            "file_hash": file_hash
                        }

                        # Add item to the appropriate category based on classification
                        if sub == "top":
                            st.session_state.tops.append(item)
                        elif sub == "bottom":
                            st.session_state.bottoms.append(item)
                        elif sub == "foot":
                            st.session_state.shoes.append(item)

                        st.success(f"Added {sub}: {info}")
                        new_hashes.add(file_hash)
                    except Exception as e:
                        st.error(f"Error processing {uploaded_file.name}: {str(e)}")

            if new_hashes:
                st.session_state.processed_hashes.update(new_hashes)
                st.session_state.uploader_key += 1
                st.rerun()

        # --------------------------
        # Manually Re-Add Deleted Item
        # --------------------------
        st.header("🔄 Re-Add Deleted Item")

        re_add_name = st.text_input("Item Name")
        re_add_category = st.selectbox("Category", ["Top", "Bottom", "Shoe"])
        re_add_season = st.selectbox("Season", ["Spring", "Summer", "Autumn", "Winter"])
        re_add_style = st.selectbox("Style" , ["Casual", "Formal", "Sport"])
        re_add_image = st.file_uploader("Upload Image", type=["png", "jpg", "jpeg"])

        if st.button("✅ Add Item"):
            if not re_add_name or not re_add_style or not re_add_image:
                st.warning("⚠️ Please fill in all fields and upload an image.")
            else:
                file_path = save_uploaded_file(re_add_image)
                if file_path:
                    item = {
                        "id": str(uuid.uuid4()),
                        "name": re_add_name,
                        "season": re_add_season.lower(),
                        "style": re_add_style.lower(),
                        "thumbnail": Image.open(file_path).resize((100, 100)),
                        "file_hash": compute_file_hash(re_add_image)
                    }

                    # Add item to the appropriate category based on selection
                    if re_add_category.lower() == "top":
                        st.session_state.tops.append(item)
                    elif re_add_category.lower() == "bottom":
                        st.session_state.bottoms.append(item)
                    elif re_add_category.lower() == "shoe":
                        st.session_state.shoes.append(item)

                    st.success(f"✅ Successfully re-added: {re_add_name} ({re_add_category})")


    # Display Items
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("👚 Tops Collection")
        display_category(st.session_state.tops, "tops")

    with col2:
        st.subheader("👖 Bottoms Collection")
        display_category(st.session_state.bottoms, "bottoms")

    with col3:
        st.subheader("👟 Shoes Collection")
        display_category(st.session_state.shoes, "shoes")

    st.markdown("---")

    # Outfit Recommendation Button
    if st.button("✨ Generate Smart Outfit Recommendation"):
        if not st.session_state.tops or not st.session_state.bottoms or not st.session_state.shoes:
            st.warning("Please add items in all categories first!")
            return

        current_season = get_current_season()

        top = random.choice(st.session_state.tops)
        bottom = random.choice(st.session_state.bottoms)
        shoe = random.choice(st.session_state.shoes)

        st.subheader("🌟 Today's Perfect Outfit")
        cols = st.columns(3)
        for idx, (item, title) in enumerate(zip([top, bottom, shoe], ["Top", "Bottom", "Shoes"])):
            with cols[idx]:
                st.markdown(f"### {title}")
                st.image(item["thumbnail"], use_container_width=True)
               # st.markdown(f" **{item['name']}**\n\n-**Style:** {item['style'].title()}\n- **Season:** {item['season'].title()}")
                clean_name = ', '.join(item["name"].split(', ')[:-1])  # Remove file path
                st.markdown(f"**{clean_name}**\n\n- **Style:** {item['style'].title()}\n- **Season:** {item['season'].title()}")
                
               # st.markdown(f" **Style:** {item['style'].title()}\n- **Season:** {item['season'].title()}")
# Run the app
if __name__ == "__main__":
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    main()

