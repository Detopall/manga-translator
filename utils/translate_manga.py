"""
This module is used to translate manga from one language to another.
"""

from deep_translator import GoogleTranslator


def translate_manga(text: str, source_lang: str = "auto", target_lang: str = "en") -> str:
    """
    Translate manga from one language to another.
    """

    if source_lang == target_lang:
        return text

    translated_text = GoogleTranslator(
        source=source_lang, target=target_lang).translate(text)
    print("Original text:", text)
    print("Translated text:", translated_text)

    return translated_text
