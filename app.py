"""
This file contains the FastAPI application that serves the web interface and handles the API requests.
"""

import os
import io
import base64

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from PIL import Image
import uvicorn
from ultralytics import YOLO

from utils.predict_bounding_boxes import predict_bounding_boxes
from utils.manga_ocr import get_text_from_images
from utils.translate_manga import translate_manga
from utils.write_text_on_image import write_text

# Load the object detection model
best_model_path = "./model_creation/runs/detect/train5"
object_detection_model = YOLO(os.path.join(best_model_path, "weights/best.pt"))

app = FastAPI()

# Add CORS middleware
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_methods=["*"],
	allow_headers=["*"]
)

# Serve static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/fonts", StaticFiles(directory="fonts"), name="fonts")
templates = Jinja2Templates(directory="templates")

@app.get("/")
def home(request: Request):
	return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
def predict(request: dict):
	image = request["image"]

	# Decode base64-encoded image
	image = base64.b64decode(image)
	image = Image.open(io.BytesIO(image))

	# Save the image
	image.save("image.jpg")

	# Perform object detection
	result = predict_bounding_boxes(object_detection_model, "image.jpg")

	# Extract text from images
	text_list = get_text_from_images("./bounding_box_images")

	# Translate the manga
	translated_text_list = translate_manga(text_list)

	# Write translation text on image
	translated_image = write_text(result, translated_text_list, "image.jpg")

	# Convert the image to base64
	buff = io.BytesIO()
	translated_image.save(buff, format="JPEG")
	img_str = base64.b64encode(buff.getvalue()).decode("utf-8")

	# Clean up
	os.remove("image.jpg")
	os.remove("translated_image.png")

	return {"image": img_str}


if __name__ == '__main__':
	uvicorn.run('app:app', host='localhost', port=8000, reload=True)
