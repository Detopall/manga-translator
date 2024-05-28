"""
This module is used to translate manga from Japanese to English.
"""
from typing import List
from deep_translator import GoogleTranslator

def translate_manga(text_list: List) -> List:
	"""
	Translate manga from Japanese to English.
	"""
	for i, text in enumerate(text_list):
		translated_text = GoogleTranslator(source="ja", target="en").translate(text)
		print("Original text:", text)
		print("Translated text:", translated_text)
		text_list[i] = translated_text
	
	return text_list
