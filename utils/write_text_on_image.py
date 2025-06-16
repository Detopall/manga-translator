"""
This module contains a function to add text to an image with a bounding box.
"""

import unicodedata
import textwrap
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2

import arabic_reshaper
from bidi.algorithm import get_display


def detect_script(text):
    """
    Detect the script of the text
    """
    scripts = set()
    for char in text:
        if char.isalpha():
            name = unicodedata.name(char, "")
            if "LATIN" in name:
                scripts.add("Latin")
            elif "ARABIC" in name:
                scripts.add("Arabic")
            elif "CYRILLIC" in name:
                scripts.add("Cyrillic")
            elif "GREEK" in name:
                scripts.add("Greek")
            elif "HEBREW" in name:
                scripts.add("Hebrew")
            elif "DEVANAGARI" in name:
                scripts.add("Devanagari")
    if not scripts:
        return "Latin"
    return list(scripts)[0]


def get_font_path(script):
    if script == "Latin":
        return "./fonts/NotoSans-Regular.ttf"
    elif script == "Arabic":
        return "./fonts/NotoNaskhArabic-Regular.ttf"
    elif script == "Cyrillic":
        return "./fonts/NotoSansCyrillic-Regular.ttf"
    elif script == "Greek":
        return "./fonts/NotoSansGreek-Regular.ttf"
    else:
        return "./fonts/NotoSans-Regular.ttf"


def add_text(image: np.ndarray, text: str, contour: np.ndarray):
    script = detect_script(text)
    font_path = get_font_path(script)
    if script == "Arabic":
        reshaped_text = arabic_reshaper.reshape(text)
        text = get_display(reshaped_text)
    pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_image)

    x, y, w, h = cv2.boundingRect(contour)

    line_height = 16
    font_size = 14
    wrapping_ratio = 0.075
    min_font_size = 6  # Minimum font size to prevent going to 0
    max_iterations = 20  # Prevent infinite loops

    wrap_width = max(1, int(w * wrapping_ratio))
    wrapped_text = textwrap.fill(text, width=wrap_width, break_long_words=True)

    font = ImageFont.truetype(font_path, size=font_size)

    lines = wrapped_text.split("\n")
    total_text_height = (len(lines)) * line_height

    iterations = 0
    while (
        total_text_height > h
        and font_size > min_font_size
        and iterations < max_iterations
    ):
        line_height = max(line_height - 2, min_font_size)
        font_size = max(font_size - 2, min_font_size)
        wrapping_ratio = min(wrapping_ratio + 0.025, 0.5)
        wrap_width = max(1, int(w * wrapping_ratio))
        wrapped_text = textwrap.fill(text, width=wrap_width, break_long_words=True)
        font = ImageFont.truetype(font_path, size=font_size)
        lines = wrapped_text.split("\n")
        total_text_height = (len(lines)) * line_height
        iterations += 1

    # If text still doesn't fit after all adjustments, truncate it
    if total_text_height > h:
        max_lines = max(1, h // line_height)
        lines = lines[:max_lines]
        if len(lines) < len(wrapped_text.split("\n")):
            # Add ellipsis to last line if text was truncated
            if lines:
                lines[-1] = lines[-1][: max(0, len(lines[-1]) - 3)] + "..."

    # Vertical centering
    actual_text_height = len(lines) * line_height
    text_y = y + max(0, (h - actual_text_height) // 2)

    for line in lines:
        text_length = draw.textlength(line, font=font)
        text_x = x + max(
            0, (w - text_length) // 2
        )  # Ensure x coordinate is not negative
        draw.text((text_x, text_y), line, font=font, fill=(0, 0, 0))
        text_y += line_height

    image[:, :, :] = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
