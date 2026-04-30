# translations.py

# A dictionary containing translations for the common strings used in the application
translations = {
    'en': {
        'greeting': 'Hello',
        'farewell': 'Goodbye',
        'thank_you': 'Thank you',
    },
    'hi': {
        'greeting': 'नमस्ते',
        'farewell': 'अलविदा',
        'thank_you': 'धन्यवाद',
    },
    'gu': {
        'greeting': 'નમસ્તે',
        'farewell': 'અલવિદા',
        'thank_you': 'ધન્યવાદ',
    }
}

# Function to get the translation of a string based on the language code

def get_translation(key, lang='en'):
    """
    Get the translation for a given key based on the language code.

    :param key: The key for the translation string
    :param lang: The language code (default is English)
    :return: The translated string or the key if not found
    """
    if lang in translations:
        return translations[lang].get(key, key)
    return key
