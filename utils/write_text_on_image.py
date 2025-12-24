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
    """Get the appropriate font path for the detected script with fallbacks"""
    import os
    
    comprehensive_fonts = [
        "/usr/share/fonts/google-noto-vf/NotoSans[wght].ttf",
        "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/google-noto/NotoSans-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/google-droid-sans-fonts/DroidSans.ttf",
    ]
    
    script_specific_fonts = {
        "Arabic": ["/usr/share/fonts/google-noto-vf/NotoSansArabic[wght].ttf",
                   "./fonts/NotoNaskhArabic-Regular.ttf"],
        "Cyrillic": ["./fonts/NotoSansCyrillic-Regular.ttf"],
        "Greek": ["./fonts/NotoSansGreek-Regular.ttf"],
    }
    
    if script in script_specific_fonts:
        for font in script_specific_fonts[script]:
            if os.path.exists(font):
                print(f"Using script-specific font for {script}: {font}")
                return font
    
    for font in comprehensive_fonts:
        if os.path.exists(font):
            print(f"Using comprehensive Unicode font: {font}")
            return font
    
    local_fonts = [
        "./fonts/NotoSans-Regular.ttf",
        "./fonts/NotoNaskhArabic-Regular.ttf",
    ]
    
    for font in local_fonts:
        if os.path.exists(font):
            print(f"Using local font: {font}")
            return font
    
    system_fallbacks = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/Windows/Fonts/arial.ttf",
    ]
    
    for fallback in system_fallbacks:
        if os.path.exists(fallback):
            print(f"Using system fallback: {fallback}")
            return fallback
    
    print("WARNING: No suitable font found, using default")
    return "./fonts/NotoSans-Regular.ttf"


def add_text(image: np.ndarray, text: str, contour: np.ndarray):
    script = detect_script(text)
    font_path = get_font_path(script)
    
    print(f"Detected script: {script}")
    print(f"Using font: {font_path}")
    print(f"Text to render: {text}")
    
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

    # Try to load font with error handling
    try:
        font = ImageFont.truetype(font_path, size=font_size)
        print(f"Successfully loaded font: {font_path}")
    except Exception as e:
        print(f"Error loading font {font_path}: {e}")
        print("Falling back to default font")
        font = ImageFont.load_default()

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
        
        try:
            font = ImageFont.truetype(font_path, size=font_size)
        except Exception:
            font = ImageFont.load_default()
        
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
        try:
            text_length = draw.textlength(line, font=font)
        except Exception:
            # Fallback for older PIL versions
            text_length = len(line) * font_size * 0.6
        
        text_x = x + max(
            0, (w - text_length) // 2
        )  # Ensure x coordinate is not negative
        
        try:
            draw.text((text_x, text_y), line, font=font, fill=(0, 0, 0))
            print(f"Drew text: '{line}' at ({text_x}, {text_y})")
        except Exception as e:
            print(f"Error drawing text '{line}': {e}")
        
        text_y += line_height

    image[:, :, :] = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
