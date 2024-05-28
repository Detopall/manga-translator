"""
This module is used to write text on an image.
"""
import os
from typing import List, Tuple
from PIL import Image, ImageFont, ImageDraw
from PIL.ImageFont import FreeTypeFont
from ultralytics import YOLO


def get_font(image: Image, text: str, width: int, height: int) -> Tuple[FreeTypeFont, int, int]:
	"""
	Get the font size and position for the text.
	"""

	# Default values at start
	font_size = None 
	font = None
	box = None  # For version 8.0.0
	x = 0
	y = 0

	draw = ImageDraw.Draw(image)  # Create a draw object

	# Test for different font sizes
	for size in range(1, 500):

		# Create new font
		new_font = ImageFont.load_default(size=font_size)

		# Calculate bbox for version 8.0.0
		new_box = draw.textbbox((0, 0), text, font=new_font)

		# Calculate width and height
		new_w = new_box[2] - new_box[0]  # Bottom - Top
		new_h = new_box[3] - new_box[1]  # Right - Left

		# If too big then exit with previous values
		if new_w > width or new_h > height:
			break

		# Set new current values as current values
		font_size = size
		font = new_font
		box = new_box
		w = new_w
		h = new_h

		# Calculate position (minus margins in box)
		x = (width - w) // 2 - box[0]  # Minus left margin
		y = (height - h) // 2 - box[1]  # Minus top margin

	return font, x, y


def add_discoloration(color: Tuple[int, int, int], strength: int) -> Tuple[int, int, int]:
	"""
	Add discoloration to the background color.
	"""

	r, g, b = color
	r = max(0, min(255, r + strength))
	g = max(0, min(255, g + strength))
	b = max(0, min(255, b + strength))

	if r == 255 and g == 255 and b == 255:
		r, g, b = 245, 245, 245

	return (r, g, b)


def get_background_color(image: Image, x_min: float,
						y_min: float, x_max: float, y_max: float) -> Tuple[int, int, int]:
	"""
	Determine the background color of the text box.
	"""

	margin = 10
	edge_region = image.crop(
		(x_min - margin, y_min - margin, x_max + margin, y_max + margin))

	# Find the most common color in the cropped region
	edge_colors = edge_region.getcolors(
		edge_region.size[0] * edge_region.size[1])
	background_color = max(edge_colors, key=lambda x: x[0])[1]

	# Add a bit of discoloration to the background color
	background_color = add_discoloration(background_color, 40)

	return background_color


def get_text_fill_color(background_color: Tuple[int, int, int]):
	"""
	Determine the text color based on the background color.
	"""
	luminance = (
		0.299 * background_color[0]
		+ 0.587 * background_color[1]
		+ 0.114 * background_color[2]
	) / 255

	# Determine the text color based on the background luminance
	if luminance > 0.5:
		return "black"
	else:
		return "white"


def translated_words_fit(translated_text: str, font: ImageFont,
						width: float, draw: ImageDraw) -> Tuple[bool, float]:
	"""
	Check if the translated words fit within the bounding box.
	"""
	words = translated_text.split()
	total_width = 0

	for word in words:
		bbox = draw.textbbox((0, 0), word, font=font)
		word_width = bbox[2] - bbox[0]
		total_width += word_width

	return total_width <= width, total_width


def recalculate_words_and_size(translated_text: List, font: ImageFont,
							image: Image, total_width: float,
							draw: ImageDraw, x_min: float, y_min: float,
							x_max: float, y_max: float) -> List:
	"""
	Recalculate the words and font size to fit within the bounding box.
	"""
	words = translated_text.split()
	even_split = total_width // len(words)
	lines = []
	current_line = ""

	for word in words:
		bbox = draw.textbbox((0, 0), word, font=font)
		word_width = bbox[2] - bbox[0]
		if len(current_line) + word_width > even_split:
			lines.append(current_line)
			current_line = word
		else:
			current_line += " " + word
	lines.append(current_line)
	translated_text = "\n".join(lines)

	# Calculate font size and position again
	font, x, y = get_font(image, translated_text, x_max - x_min, y_max - y_min)
	return translated_text, font, x, y


def replace_text_with_translation(image: Image, text_boxes: List, translated_texts: List) -> Image:
	"""
	Replace the text in the bounding boxes with the translated text.
	"""

	draw = ImageDraw.Draw(image)

	for text_box, translated_text in zip(text_boxes, translated_texts):
		x_min, y_min, x_max, y_max = text_box

		if translated_text is None:
			continue

		# Find the most common color in the text region
		background_color = get_background_color(
			image, x_min, y_min, x_max, y_max)

		# Draw a rectangle to cover the text region with the original background color
		draw.rectangle(((x_min, y_min), (x_max, y_max)), fill=background_color)

		# Calculate font size and position
		font, x, y = get_font(image, translated_text,
							x_max - x_min, y_max - y_min)

		# Split the words if they are too long
		fits, total_width = translated_words_fit(
			translated_text, font, x_max - x_min, draw)

		if not fits or font.size < 30:
			translated_text, font, x, y = recalculate_words_and_size(
				translated_text, font, image, total_width, draw, x_min, y_min, x_max, y_max)

		# Use local font
		# Get full path to the font file
		font_path = os.path.join(os.path.dirname(__file__), "../fonts/mangat.ttf")
		font = ImageFont.truetype(
			font=font_path, size=font.size, encoding="unic")

		# Draw the translated text within the box
		draw.text(
			(x_min + x, y_min + y),
			translated_text,
			fill=get_text_fill_color(background_color),
			font=font,
		)

	return image


def write_text(result: YOLO, text_list: List[str], image_path: str) -> None:
	"""
	Replace the text in the bounding boxes with the translated text.
	"""

	all_boxes = []
	all_translated_texts = []

	for i, box in enumerate(result.boxes):
		coords = [round(x) for x in box.xyxy[0].tolist()]
		text = text_list[i]

		all_boxes.append(coords)
		all_translated_texts.append(text)

	image = Image.open(image_path)

	# Draw text within all bounding boxes
	image = replace_text_with_translation(
		image, all_boxes, all_translated_texts)

	# save the image
	image.save("translated_image.png")

	return image
