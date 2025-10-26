# OutfitX-Project

# 👗 OutfitX – AI-Powered Outfit Recommendation System

## 🧠 Overview
**OutfitX** is an intelligent fashion recommendation system that helps users find complementary outfit items based on uploaded images or text inputs.  
The system analyzes outfit colors, detects fashion categories, and recommends matching items (e.g., if a user uploads a shirt, it suggests pants, shoes, and accessories) using **color theory**, **CNN-based classification**, and **complementary color mapping**.

---

## 🚀 Features
- 🖼️ Upload outfit images and get matching recommendations  
- 🎨 Color-based compatibility using **HSV color model & color theory**  
- 🤖 Deep learning-based clothing classification using **ResNet-50**  
- 🌤️ Context-aware suggestions based on **season** and **style**  
- 🧩 Streamlit interface for interactive experience  
- ☁️ Deployed on **Hugging Face Spaces**  

---

## 🧰 Tech Stack
- **Python**, **TensorFlow/Keras**, **OpenCV**, **Scikit-learn**
- **ResNet-50** pretrained model for image classification  
- **Streamlit** for front-end interface  
- **Color Theory Module** (custom HSV-based color matching)  
- **Pandas**, **NumPy**, **Matplotlib** for preprocessing and visualization  

---

## 🧩 Project Architecture
1. **Image Input** – User uploads an outfit image.  
2. **Feature Extraction** – Model classifies item category using ResNet-50.  
3. **Color Analysis** – HSV-based complementary color mapping.  
4. **Recommendation Engine** – Suggests best-matched items (pants, shoes, accessories).  
5. **Frontend Display** – Streamlit displays recommended items with confidence scores.  

---

## 🧪 Model Training
- Dataset: **Fashion Product Images Dataset (Kaggle, 44K images)**  
- Image size: 2400×1600 high-resolution product images  
- Model: **ResNet-50 (transfer learning)**  
- Optimizer: Adam | Loss: categorical_crossentropy  
- Accuracy: ~92% on validation data  

---

## ⚙️ How to Run Locally
```bash
git clone https://github.com/yourusername/OutfitX.git
cd OutfitX
pip install -r requirements.txt
streamlit run app.py
