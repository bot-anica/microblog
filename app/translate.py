from deep_translator import DeeplTranslator
from flask import current_app
from flask_babel import _


def translate(text, source_language, target_language):
    print(current_app.config['DEEPL_TRANSLATOR_KEY'])

    if not current_app.config['DEEPL_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured')

    translated = DeeplTranslator(api_key=current_app.config['DEEPL_TRANSLATOR_KEY'], source=source_language,
                                 target=target_language, use_free_api=True).translate(text)

    return translated
