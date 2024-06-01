"""
This module is used to translate manga from Japanese to English.
"""

from deep_translator import GoogleTranslator

def translate_manga(text: str) -> str:
	"""
	Translate manga from Japanese to English.
	"""
	translated_text = GoogleTranslator(source="ja", target="en").translate(text)
	print("Original text:", text)
	print("Translated text:", translated_text)
	
	return translated_text
