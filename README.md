# Manga Translator

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Approach](#approach)
  - [Data Collection](#data-collection)
  - [Yolov8](#yolov8)
  - [Manga-ocr](#manga-ocr)
  - [Deep-translator](#deep-translator)
- [Server](#server)
- [Usage](#usage)
- [Known Limitations](#known-limitations)
- [Demo](#demo)

## Introduction

I love reading manga, and I can't wait for the next chapter of my favorite manga to be released. However, the newest chapters are usually in Japanese, and they are translated to English after some time. I want to read the newest chapters as soon as possible, so I decided to build a manga translator that can translate Japanese manga to English.

**NEW**: The application now supports multiple languages including Arabic, Greek, Cyrillic, and other non-Latin scripts, with customizable source and target language selection!

> [!INFO] Tested using Python3.12

## Features

### Core Translation

- **Automatic Speech Bubble Detection** - Uses YOLOv8 to identify text regions
- **OCR Text Extraction** - Extracts Japanese text using manga-ocr
- **Multi-language Translation** - Translate between 300+ languages
- **Batch Processing** - Upload and translate multiple manga pages at once

### User Interface

- **Modern Web Interface** - Clean, responsive design
- **Carousel Navigation** - View translated pages one at a time with arrow keys
- **Mobile Optimized** - Fully responsive for phones and tablets
- **Image Zoom** - Click any image to view in fullscreen
- **Language Selection** - Choose both source and target languages
- **Zip Download** - Download all translated images as a single zip file

### Performance

- **GPU Acceleration** - Automatically uses GPU if available, falls back to CPU
- **Fast Processing** - Optimized for quick translation

## Approach

I want to translate the text in the manga images from Japanese to English. I will first need to know where these speech bubbles are on the image. For this I will use `Yolov8` to detect the speech bubbles. Once I have the speech bubbles, I will use `manga-ocr` to extract the text from the speech bubbles. Finally, I will use `deep-translator` to translate the text from Japanese to English.

![Manga Translator](./assets/MangaTranslator.png)

### Data Collection

This [dataset](https://universe.roboflow.com/speechbubbledetection-y9yz3/bubble-detection-gbjon/dataset/2#) contains over 8500 images of manga pages together with their annotations from Roboflow. I will use this dataset to train `Yolov8` to detect the speech bubbles in the manga images. To use this dataset with Yolov8, I will need to convert the annotations to the YOLO format, which is a text file containing the class label and the bounding box coordinates of the object in the image.

This dataset is over 1.7GB in size, so I will need to download it to my local machine. The rest of the code should be run after the dataset has been downloaded and extracted in this directory.

The dataset contains mostly English manga, but that is fine since I am only interested in the speech bubbles.

### Yolov8

`Yolov8` is a state-of-the-art, real-time object detection system [that I've used in the past before](https://github.com/Detopall/parking-lot-prediction). I will use `Yolov8` to detect the speech bubbles in the manga images.

### Manga-ocr

Optical character recognition for Japanese text, with the main focus being Japanese manga. This Python package is built and trained specifically for extracting text from manga images. This makes it perfect for extracting text from the speech bubbles in the manga images.

### Deep-translator

`Deep-translator` is a Python package that uses the Google Translate API to translate text from one language to another. I will use `deep-translator` to translate the text extracted from the manga images from Japanese to English.

## Server

I created a simple server and client using FastAPI. The server will receive manga images from the client, detect the speech bubbles, extract the text from the speech bubbles, and translate the text to the target language. The server will then send the translated images back to the client.

To run the server, you will need to install the required packages. You can do this by running the following command:

```bash
pip install -r requirements.txt
```

You can then start the server by running the following command:

```bash
python app.py
```

The server will start running on `http://localhost:8000`. You can access the web interface by opening this URL in your browser.

## Usage

1. **Open the web interface** at `http://localhost:8000`
2. **Select source language** (defaults to Japanese)
3. **Select target language** (defaults to English)
4. **Upload one or more manga images** using the file selector
5. **Click "Translate"** to process the images
6. **Navigate results** using:
    - Left/Right arrow buttons on screen
    - Keyboard arrow keys (<- ->)
    - Click any image to view in fullscreen
7. **Download results** using the "Download All as Zip" button

### API Endpoint

You can also use the API directly:

```json
POST /predict
{
  "images": ["base64_encoded_image1", "base64_encoded_image2"],
  "source_lang": "ja-JP",
  "target_lang": "en-US"
}
```

## Known Limitations

### OCR Accuracy

- The OCR model is optimized for Japanese manga and may struggle with:
  - **Cyrillic alphabets** - May not fully recognize or translate correctly
  - **Stylized fonts** - Artistic or decorative text may be misread
  - **Low-quality images** - Blurry or low-resolution images reduce accuracy
  - **Vertical text** - Some vertical text layouts may be challenging

### Translation Quality

- Translation quality depends on the source text clarity
- Garbled OCR output will result in poor translations
- Some context-specific phrases may not translate accurately
- Mixed scripts (e.g., Japanese + English) may cause issues

### Recommendations

- Use high-quality, clear manga images
- Black and white images work best
- Ensure text is clearly visible and not too stylized
- For best results, use Japanese manga with standard fonts

## Demo

The following video is a screen recording of the client sending a manga image to the server, and the server detecting the speech bubbles, extracting the text, and translating the text from Japanese to English. (Currently, an older version of the application is used)

[![Manga Translator](./assets/MangaTranslator.png)](https://www.youtube.com/watch?v=P0VZu4whrz4)
