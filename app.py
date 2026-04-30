import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import json
from translations import TRANSLATIONS, get_translation
from googletrans import Translator

# Initialize Translator
translator = Translator()

st.set_page_config(page_title="AgriVision", page_icon="🌿", layout="wide")

if 'language' not in st.session_state:
    st.session_state.language = 'en'

def t(key):
    return get_translation(key, st.session_state.language)

def translate_text(text, target_lang):
    if target_lang == 'en' or not text: return text
    try:
        return translator.translate(text, dest=target_lang).text
    except:
        return text

@st.cache_resource
def load_assets():
    interpreter = tf.lite.Interpreter(model_path='plant_disease_model.tflite')
    interpreter.allocate_tensors()
    with open('class_indices.json', 'r') as f:
        classes = {v: k for k, v in json.load(f).items()}
    with open('treatment_database.json', 'r') as f:
        db = json.load(f)
    return interpreter, classes, db

def predict_disease(interpreter, image):
    input_det = interpreter.get_input_details()
    img = image.resize((224, 224))
    img_array = np.expand_dims(np.array(img)/255.0, axis=0).astype(np.float32)
    interpreter.set_tensor(input_det[0]['index'], img_array)
    interpreter.invoke()
    return interpreter.get_tensor(interpreter.get_output_details()[0]['index'])[0]

def main():
    st.markdown('<h1 style="text-align:center; color:#2E7D32;">🌿 AgriVision</h1>', unsafe_allow_html=True)
    interpreter, index_to_class, treatment_db = load_assets()

    # Sidebar
    with st.sidebar:
        st.header("🌐 Language")
        lang_sel = st.selectbox("Language", ["English", "हिंदी (Hindi)", "ગુજરાતી (Gujarati)"], index=0)
        st.session_state.language = {"English":"en", "हिंदी (Hindi)":"hi", "ગુજરાતી (Gujarati)":"gu"}[lang_sel]
        
        st.divider()
        st.header(t('model_info_title'))
        st.info(f"🎯 {t('accuracy')}: 98.5%\n\n📦 {t('classes')}: 38\n\n💾 {t('model_size')}: 2.7MB")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.header(t('upload_title'))
        uploaded_file = st.file_uploader(t('upload_description'), type=['jpg', 'jpeg', 'png'])
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)
            if st.button(t('analyze_button'), type="primary", use_container_width=True):
                with st.spinner(t('analyzing')):
                    preds = predict_disease(interpreter, image)
                    idx = np.argmax(preds)
                    st.session_state.results = {'name': index_to_class[idx], 'conf': preds[idx]}
        else:
            # CONTENT FOR EMPTY STATE
            st.markdown(f"### {t('welcome_title')}")
            st.write(t('welcome_desc'))
            st.markdown(f"**{t('how_it_works')}**")
            st.write(f"{t('step_1')}\n{t('step_2')}\n{t('step_3')}")
            st.image("https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?auto=format&fit=crop&w=800&q=80", caption="Healthy Farming")

    with col2:
        st.header(t('results_title'))
        if 'results' in st.session_state:
            res = st.session_state.results
            info = treatment_db.get(res['name'], treatment_db['default'])
            l = st.session_state.language
            
            st.success(f"### 🦠 {res['name']}")
            st.metric(t('confidence'), f"{res['conf']*100:.1f}%")
            
            with st.expander(t('description'), expanded=True):
                st.write(translate_text(info['description'], l))

            st.subheader(t('treatment_title'))
            tb = st.tabs([t('organic_tab'), t('chemical_tab'), t('prevention_tab')])
            
            org = [translate_text(i, l) for i in info['organic_treatment']]
            chem = [translate_text(i, l) for i in info['chemical_treatment']]
            prev = [translate_text(i, l) for i in info['prevention']]

            with tb[0]:
                for i in org:
                    st.write(f"🌱 {i}")
            with tb[1]:
                for i in chem:
                    st.write(f"🧪 {i}")
            with tb[2]:
                for i in prev:
                    st.write(f"🛡️ {i}")

            # DETAILED DOWNLOADABLE REPORT
            full_report = f"""
{t('report_header')}
====================================
{t('disease_label')}: {res['name']}
{t('confidence')}: {res['conf']*100:.1f}%

{t('description').upper()}:
{translate_text(info['description'], l)}

{t('organic_treatments').upper()}:
{chr(10).join(['- ' + i for i in org])}

{t('chemical_treatments').upper()}:
{chr(10).join(['- ' + i for i in chem])}

{t('prevention_measures').upper()}:
{chr(10).join(['- ' + i for i in prev])}

------------------------------------
{t('report_footer')}
            """
            st.download_button(
                label=t('download_button'), # This now uses the translation key!
                data=full_report,
                file_name=f"AgriVision_{res['name']}.txt",
                mime="text/plain",
                use_container_width=True
            )
        else:
            st.info(t('result_prompt'))

if __name__ == "__main__":
    main()
