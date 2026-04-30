# translations.py

# A dictionary containing translations for the common strings used in the application
# Named TRANSLATIONS in uppercase to match your app.py import
TRANSLATIONS = {
    'en': {
        'subtitle': 'AI-Powered Plant Health Analysis',
        'about_title': 'About AgriVision',
        'about_description': 'AgriVision helps farmers identify plant diseases quickly and accurately using deep learning. Simply upload an image of a plant leaf, and our AI will provide a diagnosis and treatment suggestions.',
        'model_info_title': 'Model Information',
        'accuracy': 'Accuracy',
        'classes': 'Supported Classes',
        'model_size': 'Model Size',
        'upload_title': 'Upload Leaf Image',
        'upload_description': 'Select a clear photo of the plant leaf for analysis.',
        'upload_prompt': 'Please upload an image to start analysis',
        'results_title': 'Analysis Results',
        'result_prompt': 'Results will appear here after analysis',
        'tips_title': 'Photography Tips',
        'tips_description': '• Ensure the leaf is well-lit.\n• Focus on the affected part of the leaf.\n• Keep the camera steady.',
        'tagline': 'Empowering Agriculture through AI',
        'disclaimer': 'Disclaimer: This tool is for educational purposes. Consult an agricultural expert for critical decisions.',
        'greeting': 'Hello',
        'farewell': 'Goodbye',
        'thank_you': 'Thank you',
    },
    'hi': {
        'subtitle': 'AI-संचालित पौधा स्वास्थ्य विश्लेषण',
        'about_title': 'एग्रीविजन के बारे में',
        'about_description': 'एग्रीविजन किसानों को डीप लर्निंग का उपयोग करके पौधों की बीमारियों की जल्दी और सटीक पहचान करने में मदद करता है। बस एक पौधे की पत्ती की छवि अपलोड करें, और हमारा AI निदान और उपचार सुझाव प्रदान करेगा।',
        'model_info_title': 'मॉडल की जानकारी',
        'accuracy': 'सटीकता',
        'classes': 'समर्थित श्रेणियां',
        'model_size': 'मॉडल का आकार',
        'upload_title': 'पत्ती की छवि अपलोड करें',
        'upload_description': 'विश्लेषण के लिए पौधे की पत्ती का स्पष्ट फोटो चुनें।',
        'upload_prompt': 'विश्लेषण शुरू करने के लिए कृपया एक छवि अपलोड करें',
        'results_title': 'विश्लेषण के परिणाम',
        'result_prompt': 'विश्लेषण के बाद परिणाम यहाँ दिखाई देंगे',
        'tips_title': 'फोटोग्राफी टिप्स',
        'tips_description': '• सुनिश्चित करें कि पत्ती पर अच्छी रोशनी हो।\n• पत्ती के प्रभावित हिस्से पर ध्यान केंद्रित करें।\n• कैमरे को स्थिर रखें।',
        'tagline': 'AI के माध्यम से कृषि को सशक्त बनाना',
        'disclaimer': 'अस्वीकरण: यह उपकरण शैक्षिक उद्देश्यों के लिए है। महत्वपूर्ण निर्णयों के लिए कृषि विशेषज्ञ से सलाह लें।',
        'greeting': 'नमस्ते',
        'farewell': 'अलविदा',
        'thank_you': 'धन्यवाद',
    },
    'gu': {
        'subtitle': 'AI-સંચાલિત છોડ આરોગ્ય વિશ્લેષણ',
        'about_title': 'AgriVision વિશે',
        'about_description': 'AgriVision ખેડૂતોને ડીપ લર્નિંગનો ઉપયોગ કરીને છોડના રોગોને ઝડપથી અને સચોટ રીતે ઓળખવામાં મદદ કરે છે. ફક્ત છોડના પાનનો ફોટો અપલોડ કરો, અને અમારું AI નિદાન અને સારવારના સૂચનો આપશે.',
        'model_info_title': 'મોડેલ માહિતી',
        'accuracy': 'ચોકસાઈ',
        'classes': 'સપોર્ટેડ ક્લાસિસ',
        'model_size': 'મોડેલ કદ',
        'upload_title': 'પાનની છબી અપલોડ કરો',
        'upload_description': 'વિશ્લેષણ માટે છોડના પાનનો સ્પષ્ટ ફોટો પસંદ કરો.',
        'upload_prompt': 'વિશ્લેષણ શરૂ કરવા માટે કૃપા કરીને છબી અપલોડ કરો',
        'results_title': 'વિશ્લેષણ પરિણામો',
        'result_prompt': 'વિશ્લેષણ પછી પરિણામો અહીં દેખાશે',
        'tips_title': 'ફોટોગ્રાફી ટિપ્સ',
        'tips_description': '• પાન પર સારી રોશની હોવાની ખાતરી કરો.\n• પાનના પ્રભાવિત ભાગ પર ધ્યાન કેન્દ્રિત કરો.\n• કેમેરા સ્થિર રાખો.',
        'tagline': 'AI દ્વારા કૃષિનું સશક્તિકરણ',
        'disclaimer': 'ડિસ્ક્લેમર: આ સાધન શૈક્ષણિક હેતુઓ માટે છે. મહત્વપૂર્ણ નિર્ણયો માટે કૃષિ નિષ્ણાતની સલાહ લો.',
        'greeting': 'નમસ્તે',
        'farewell': 'અલવિદા',
        'thank_you': 'ધન્યવાદ',
    }
}

def get_translation(key, lang='en'):
    """
    Get the translation for a given key based on the language code.
    """
    if lang in TRANSLATIONS:
        return TRANSLATIONS[lang].get(key, key)
    return key
