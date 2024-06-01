"""
This module is used to predict bounding boxes for text
in images using the trained Object Detection model.
"""
import uuid
import os
from typing import List
from PIL import Image
from ultralytics import YOLO

def predict_bounding_boxes(model: YOLO, image_path: str) -> List:
	"""
	Predict bounding boxes for text in images using the trained Object Detection model.
	"""

	image = Image.open(image_path)
	bounding_box_images_path = "./bounding_box_images"

	# Create the directory if it doesn't exist
	if not os.path.exists(bounding_box_images_path):
		os.makedirs(bounding_box_images_path)

	# Clear the directory
	for file in os.listdir(bounding_box_images_path):
		os.remove(os.path.join(bounding_box_images_path, file))

	# Perform inference
	result = model.predict(image_path)[0]

	for box in result.boxes:
		label = result.names[box.cls[0].item()]
		coords = [round(x) for x in box.xyxy[0].tolist()]
		prob = round(box.conf[0].item(), 4)
		print("Object: {}\nCoordinates: {}\nProbability: {}".format(label, coords, prob))
		cropped_image = image.crop(coords)

		# save each image under a unique name
		cropped_image.save(f"{bounding_box_images_path}/{uuid.uuid4()}.png")
	
	return result.boxes.data.tolist()
