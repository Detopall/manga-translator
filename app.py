"""
This file contains the FastAPI application that serves the web interface and handles the API requests.
"""

import os
import io
import base64
from typing import Dict

import numpy as np
from fastapi import FastAPI
from fastapi import status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from PIL import Image
import uvicorn
from ultralytics import YOLO

from utils.predict_bounding_boxes import predict_bounding_boxes
from utils.manga_ocr import get_text_from_image
from utils.translate_manga import translate_manga
from utils.process_contour import process_contour
from utils.write_text_on_image import add_text


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
def predict(request: Dict):
	try:

		image = request["image"]

		image_info = {
			"detected_language": "",
			"translated_language": "",
			"bounding_boxes": [],
			"text": [],
			"translated_text": []
		}

		# Decode base64-encoded image
		image = base64.b64decode(image)
		image = Image.open(io.BytesIO(image))
		image_path = "image.png"
		translated_image_path = "translated_image.png"

		# Save the image locally
		image.save(image_path)

		results = predict_bounding_boxes(object_detection_model, image_path)
		image = np.array(image)

		for result in results:
				x1, y1, x2, y2, _, _ = result
				detected_image = image[int(y1):int(y2), int(x1):int(x2)]
				im = Image.fromarray(np.uint8((detected_image)*255))
				text = get_text_from_image(im)
				detected_image, cont = process_contour(detected_image)
				text_translated = translate_manga(text, source_lang="auto", target_lang="en")
				add_text(detected_image, text_translated, cont)

				image_info["bounding_boxes"].append(result)
				image_info["text"].append(text)
				image_info["translated_text"].append(text_translated)
				image_info["detected_language"] = "auto"
				image_info["translated_language"] = "en"


		# Display the translated image
		result_image = Image.fromarray(image, 'RGB')
		result_image.save(translated_image_path)

		# Convert the image to base64
		buff = io.BytesIO()
		result_image.save(buff, format="PNG")
		img_str = base64.b64encode(buff.getvalue()).decode("utf-8")

		# Clean up
		os.remove(image_path)
		os.remove(translated_image_path)

		return {"image": img_str, "image_info": image_info}

	except Exception as e:
		# Return with status code 500 (Internal Server Error) if an error occurs
		return JSONResponse(
                status_code=500,
                content={
                         "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                         "message": "Internal Server Error"}
            )

if __name__ == '__main__':
	uvicorn.run('app:app', host='localhost', port=8000, reload=True)
