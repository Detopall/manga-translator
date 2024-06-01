"""
This module is used to extract text from images using manga_ocr.
"""

from manga_ocr import MangaOcr


def get_text_from_image(image):
	"""
	Extract text from images using manga_ocr.
	"""
	mocr = MangaOcr()

	return mocr(image)
