"""
This module is used to extract text from images using pytesseract.
"""

import os
from typing import List
from manga_ocr import MangaOcr

def get_text_from_images(bounding_box_images_path: str) -> List[str]:
	"""
	Extract text from images using pytesseract.
	"""
	mocr = MangaOcr()

	text_list = []

	for image_path in os.listdir(bounding_box_images_path):
		image_path = os.path.join(bounding_box_images_path, image_path)
		text = mocr(image_path)
		text_list.append(text)

	return text_list
