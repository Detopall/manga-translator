"""
This module is used to translate manga from one language to another.
"""

from deep_translator import MyMemoryTranslator


def translate_manga(text: str, target_lang: str, source_lang: str = "ja-JP") -> str:
    """
    Translate manga from one language to another.
    """

    if source_lang == target_lang:
        return text

    if text == "．．．":
        return text

    translated_text = MyMemoryTranslator(
        source=source_lang, target=target_lang
    ).translate(text)
    print("Original text:", text)
    print("Translated text:", translated_text)

    return translated_text if translated_text != "．．．" else text
