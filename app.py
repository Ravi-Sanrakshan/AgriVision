import streamlit as st
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import os
from translations import TRANSLATIONS, get_translation

st.set_page_config(
    page_title="AgriVision - Plant Disease Detection",
    page_icon="🌿",
    layout="wide"
)

# Initialize language in session state
if 'language' not in st.session_state:
    st.session_state.language = 'en'

st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .disease-name {
        font-size: 2rem;
        color: #1976D2;
        font-weight: bold;
    }
    .confidence-score {
        font-size: 1.5rem;
        color: #388E3C;
    }
    .treatment-section {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Language selection in sidebar
with st.sidebar:
    st.header("🌐 Language Selection")
    language = st.selectbox(
        "Select Language / भाषा चुनें / ભાષા પસંદ કરો",
        options=["English", "हिंदी (Hindi)", "ગુજરાતી (Gujarati)"],
        key="language_select"
    )
    
    # Map display language to code
    lang_code = {
        "English": "en",
        "हिंदी (Hindi)": "hi",
        "ગુજરાતી (Gujarati)": "gu"
    }[language]
    
    st.session_state.language = lang_code

# Helper function to get translated text
def t(key):
    return get_translation(key, st.session_state.language)

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
        st.error(f"{t('error_loading_model')}: {str(e)}")
        return None, None, None

def preprocess_image(image):
    img = image.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0).astype(np.float32)
    return img_array

def predict_disease(interpreter, image):
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    
    processed_image = preprocess_image(image)
    interpreter.set_tensor(input_details[0]['index'], processed_image)
    interpreter.invoke()
    predictions = interpreter.get_tensor(output_details[0]['index'])
    
    return predictions[0]

def get_treatment_info(class_name, treatment_db):
    if class_name in treatment_db:
        return treatment_db[class_name]
    else:
        return treatment_db.get('default', {
            'disease_name': 'Unknown',
            'description': 'No information available',
            'organic_treatment': ['Consult an expert'],
            'chemical_treatment': ['Consult an expert'],
            'prevention': ['Regular monitoring']
        })

def generate_report(treatment_info, confidence_pct, language):
    """Generate report in the selected language"""
    if language == 'hi':
        report = f"""एग्रीविजन रोग निदान रिपोर्ट
====================================

रोग: {treatment_info['disease_name']}
आत्मविश्वास: {confidence_pct:.1f}%

विवरण:
{treatment_info['description']}

जैविक उपचार:
{chr(10).join([f"{i+1}. {t}" for i, t in enumerate(treatment_info['organic_treatment'])])}

रासायनिक उपचार:
{chr(10).join([f"{i+1}. {t}" for i, t in enumerate(treatment_info['chemical_treatment'])])}

रोकथाम:
{chr(10).join([f"{i+1}. {p}" for i, p in enumerate(treatment_info['prevention'])])}

---
AgriVision द्वारा तैयार - AI संचालित पौधा रोग निदान
"""
    elif language == 'gu':
        report = f"""એગ્રીવિજન રોગ નિદાન રિપોર્ટ
====================================

રોગ: {treatment_info['disease_name']}
આત્મવિશ્વાસ: {confidence_pct:.1f}%

વર્ણન:
{treatment_info['description']}

જૈવિક સારવાર:
{chr(10).join([f"{i+1}. {t}" for i, t in enumerate(treatment_info['organic_treatment'])])}

રાસાયણિક સારવાર:
{chr(10).join([f"{i+1}. {t}" for i, t in enumerate(treatment_info['chemical_treatment'])])}

નિવારણ:
{chr(10).join([f"{i+1}. {p}" for i, p in enumerate(treatment_info['prevention'])])}

---
AgriVision દ્વારા તૈયાર - AI આધારિત છોડ રોગ નિદાન
"""
    else:  # English
        report = f"""AGRIVISION DISEASE DIAGNOSIS REPORT
====================================

Disease: {treatment_info['disease_name']}
Confidence: {confidence_pct:.1f}%

Description:
{treatment_info['description']}

ORGANIC TREATMENT:
{chr(10).join([f"{i+1}. {t}" for i, t in enumerate(treatment_info['organic_treatment'])])}

CHEMICAL TREATMENT:
{chr(10).join([f"{i+1}. {t}" for i, t in enumerate(treatment_info['chemical_treatment'])])}

PREVENTION:
{chr(10).join([f"{i+1}. {p}" for i, p in enumerate(treatment_info['prevention'])])}

---
Generated by AgriVision - AI Plant Disease Detection
"""
    return report

def main():
    st.markdown('<h1 class="main-header">🌿 AgriVision</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">{t("subtitle")}</p>', unsafe_allow_html=True)
    
    interpreter, index_to_class, treatment_db = load_model_and_classes()
    
    if interpreter is None:
        st.error(f"❌ {t('model_load_failed')}")
        return
    
    with st.sidebar:
        st.header(t('about_title'))
        st.write(t('about_description'))
        
        st.header(t('model_info_title'))
        try:
            with open('model_metadata.json', 'r') as f:
                metadata = json.load(f)
            st.write(f"**{t('accuracy')}:** {metadata.get('test_accuracy', 0)*100:.1f}%")
            st.write(f"**{t('classes')}:** {metadata.get('num_classes', 'N/A')}")
            st.write(f"**{t('model_size')}:** {metadata.get('model_size_tflite_mb', 'N/A')} MB")
        except:
            st.write(f"**{t('framework')}:** Python + Streamlit Cloud")
            st.write(f"**{t('ml_engine')}:** Convolutional Neural Network - MobileNetV2")
            st.write(f"**{t('dataset')}:** PlantVillage")
            st.write(f"**{t('overall_accuracy')}:** 97.04%")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header(t('upload_title'))
        
        uploaded_file = st.file_uploader(
            t('upload_description'),
            type=['jpg', 'jpeg'],
            help=t('upload_help')
        )
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption=t('uploaded_image'), use_column_width=True)
            
            if st.button(t('analyze_button'), type="primary", use_container_width=True):
                with st.spinner(t('analyzing')):
                    predictions = predict_disease(interpreter, image)
                    
                    predicted_class_idx = np.argmax(predictions)
                    confidence = predictions[predicted_class_idx]
                    predicted_class_name = index_to_class[predicted_class_idx]
                    
                    top_3_indices = np.argsort(predictions)[-3:][::-1]
                    
                    st.session_state['predictions'] = predictions
                    st.session_state['predicted_class_name'] = predicted_class_name
                    st.session_state['confidence'] = confidence
                    st.session_state['top_3_indices'] = top_3_indices
        
        else:
            st.info(f"👆 {t('upload_prompt')}")
            
            st.subheader(t('tips_title'))
            st.write(t('tips_description'))
    
    with col2:
        st.header(t('results_title'))
        
        if 'predicted_class_name' in st.session_state:
            predicted_class_name = st.session_state['predicted_class_name']
            confidence = st.session_state['confidence']
            predictions = st.session_state['predictions']
            top_3_indices = st.session_state['top_3_indices']
            
            treatment_info = get_treatment_info(predicted_class_name, treatment_db)
            
            st.markdown(f'<p class="disease-name">🦠 {treatment_info["disease_name"]}</p>', unsafe_allow_html=True)
            
            confidence_pct = confidence * 100
            if confidence_pct >= 80:
                conf_color = "green"
            elif confidence_pct >= 60:
                conf_color = "orange"
            else:
                conf_color = "red"
            
            st.markdown(f'<p class="confidence-score">{t("confidence")}: <span style="color:{conf_color}">{confidence_pct:.1f}%</span></p>', unsafe_allow_html=True)
            
            st.write(f"**{t('description')}:** {treatment_info['description']}")
            
            with st.expander(t('top_predictions')):
                for idx in top_3_indices:
                    class_name = index_to_class[idx]
                    prob = predictions[idx] * 100
                    st.write(f"**{class_name}:** {prob:.1f}%")
            
            st.markdown('<div class="treatment-section">', unsafe_allow_html=True)
            st.subheader(t('treatment_title'))
            
            tab1, tab2, tab3 = st.tabs([t('organic_tab'), t('chemical_tab'), t('prevention_tab')])
            
            with tab1:
                st.write(f"**{t('organic_treatments')}:**")
                for i, treatment in enumerate(treatment_info['organic_treatment'], 1):
                    st.write(f"{i}. {treatment}")
            
            with tab2:
                st.write(f"**{t('chemical_treatments')}:**")
                for i, treatment in enumerate(treatment_info['chemical_treatment'], 1):
                    st.write(f"{i}. {treatment}")
            
            with tab3:
                st.write(f"**{t('prevention_measures')}:**")
                for i, prevention in enumerate(treatment_info['prevention'], 1):
                    st.write(f"{i}. {prevention}")
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            if confidence_pct < 70:
                st.warning(t('low_confidence_warning'))
            
            # Generate report in selected language
            report = generate_report(treatment_info, confidence_pct, st.session_state.language)
            
            filename_map = {
                'en': 'agrivision_report_en.txt',
                'hi': 'agrivision_report_hi.txt',
                'gu': 'agrivision_report_gu.txt'
            }
            
            st.download_button(
                label=t('download_button'),
                data=report,
                file_name=filename_map.get(st.session_state.language, 'agrivision_report.txt'),
                mime="text/plain"
            )
        
        else:
            st.info(f"👈 {t('result_prompt')}")
    
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; color: #666;'>
        <p>🌾 AgriVision - {t('tagline')}</p>
        <p>⚠️ {t('disclaimer')}</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
