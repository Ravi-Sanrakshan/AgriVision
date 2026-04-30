import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import os
from translations import TRANSLATIONS, get_translation
from googletrans import Translator

# Initialize Translator
translator = Translator()

st.set_page_config(page_title="AgriVision - Plant Disease Detection", page_icon="🌿", layout="wide")

# Initialize language in session state
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# Helper function to get translated UI text
def t(key):
    return get_translation(key, st.session_state.language)

# Helper function to auto-translate database content
def translate_text(text, target_lang):
    if target_lang == 'en' or not text:
        return text
    try:
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except Exception:
        return text  # Fallback to English

st.markdown("""
    <style>
    .main-header {font-size: 3rem; color: #2E7D32; text-align: center; margin-bottom: 1rem; }
    .sub-header {font-size: 1.2rem; color: #666; text-align: center; margin-bottom: 2rem; }
    .disease-name {font-size: 2rem; color: #1976D2; font-weight: bold; }
    .confidence-score {font-size: 1.5rem; color: #388E3C; }
    .treatment-section {background-color: #f0f2f6; padding: 1.5rem; border-radius: 10px; margin-top: 1rem; }
    </style>
    """, unsafe_allow_html=True)

# Language selection in sidebar
with st.sidebar:
    st.header("🌐 Language Selection")
    language = st.selectbox("Select Language", options=["English", "हिंदी (Hindi)", "ગુજરાતી (Gujarati)"], key="language_select")
    lang_code = {"English": "en", "हिंदी (Hindi)": "hi", "ગુજરાતી (Gujarati)": "gu"}[language]
    st.session_state.language = lang_code

@st.cache_resource
def load_model_and_classes():
    try:
        interpreter = tf.lite.Interpreter(model_path='plant_disease_model.tflite')
        interpreter.allocate_tensors()
        with open('class_indices.json', 'r') as f:
            class_indices = json.load(f)
        index_to_class = {v: k for k, v in class_indices.items()}
        with open('treatment_database.json', 'r') as f:
            treatment_db = json.load(f)
        return interpreter, index_to_class, treatment_db
    except Exception as e:
        return None, None, None

def predict_disease(interpreter, image):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    img = image.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0).astype(np.float32)
    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()
    return interpreter.get_tensor(output_details[0]['index'])[0]

def main():
    st.markdown('<h1 class="main-header">🌿 AgriVision</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">{t("subtitle")}</p>', unsafe_allow_html=True)
    
    interpreter, index_to_class, treatment_db = load_model_and_classes()
    if interpreter is None:
        st.error("Model load failed.")
        return

    with st.sidebar:
        st.header(t('about_title'))
        st.write(t('about_description'))

    col1, col2 = st.columns([1, 1])
    with col1:
        st.header(t('upload_title'))
        uploaded_file = st.file_uploader(t('upload_description'), type=['jpg', 'jpeg'])
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)
            if st.button(t('analyze_button'), type="primary"):
                with st.spinner(t('analyzing')):
                    preds = predict_disease(interpreter, image)
                    idx = np.argmax(preds)
                    st.session_state.results = {
                        'name': index_to_class[idx],
                        'conf': preds[idx],
                        'top3': np.argsort(preds)[-3:][::-1],
                        'all_preds': preds
                    }

    with col2:
        st.header(t('results_title'))
        if 'results' in st.session_state:
            res = st.session_state.results
            info = treatment_db.get(res['name'], treatment_db['default'])
            
            st.markdown(f'<p class="disease-name">🦠 {res["name"]}</p>', unsafe_allow_html=True)
            st.write(f"**{t('confidence')}:** {res['conf']*100:.1f}%")
            
            # Auto-translated description
            st.write(f"**{t('description')}:** {translate_text(info['description'], st.session_state.language)}")
            
            st.markdown('<div class="treatment-section">', unsafe_allow_html=True)
            st.subheader(t('treatment_title'))
            tabs = st.tabs([t('organic_tab'), t('chemical_tab'), t('prevention_tab')])
            
            with tabs[0]:
                for item in info['organic_treatment']:
                    st.write(f"🌱 {translate_text(item, st.session_state.language)}")
            with tabs[1]:
                for item in info['chemical_treatment']:
                    st.write(f"🧪 {translate_text(item, st.session_state.language)}")
            with tabs[2]:
                for item in info['prevention']:
                    st.write(f"🛡️ {translate_text(item, st.session_state.language)}")
            st.markdown('</div>', unsafe_allow_html=True)

            # Translated Download Report
            report = f"{t('report_header')}\n{t('disease_label')}: {res['name']}\n{t('description')}: {translate_text(info['description'], st.session_state.language)}"
            st.download_button(t('download_button'), report, file_name="report.txt")
        else:
            st.info(t('result_prompt'))

if __name__ == "__main__":
    main()
