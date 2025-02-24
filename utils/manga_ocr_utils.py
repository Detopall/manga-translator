"""
This module is used to extract text from images using manga_ocr.
"""

from manga_ocr import MangaOcr

mocr = MangaOcr()

def get_text_from_image(image):
	"""
	Extract text from images using manga_ocr.
	"""

	try:
		result = mocr(image)
		return result
	except Exception as e:
		print(f"An error occurred: {str(e)}")
		return None
