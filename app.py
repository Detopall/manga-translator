import os
import io
import base64
import zipfile
import torch
from typing import Dict, Any, List

import numpy as np
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from PIL import Image
import uvicorn
from ultralytics import YOLO
from fastapi.responses import StreamingResponse

from utils.predict_bounding_boxes import predict_bounding_boxes
from utils.manga_ocr_utils import get_text_from_image
from utils.translate_manga import translate_manga
from utils.process_contour import process_contour
from utils.write_text_on_image import add_text

MODEL_PATH = "./model_creation/runs/detect/train5/weights/best.pt"

# GPU Detection
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")

object_detection_model = YOLO(MODEL_PATH)
object_detection_model.to(device)

app = FastAPI()

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/fonts", StaticFiles(directory="fonts"), name="fonts")
templates = Jinja2Templates(directory="templates")


def decode_base64_image(encoded_image: str) -> Image.Image:
    decoded_bytes = base64.b64decode(encoded_image)
    image = Image.open(io.BytesIO(decoded_bytes))
    return image.convert("RGB")


def extract_text_from_regions(
    image: np.ndarray, target_lang: str, source_lang: str, results: list
) -> Dict[str, Any]:
    image_info = {
        "detected_language": "auto",
        "translated_language": "en",
        "bounding_boxes": [],
        "text": [],
        "translated_text": [],
    }

    for result in results:
        x1, y1, x2, y2, _, _ = result
        detected_image = image[int(y1) : int(y2), int(x1) : int(x2)]
        if detected_image.shape[-1] == 4:
            detected_image = detected_image[:, :, :3]
        im = Image.fromarray(np.uint8(detected_image * 255))
        text = get_text_from_image(im)

        processed_image, cont = process_contour(detected_image)
        translated_text = translate_manga(
            text, target_lang=target_lang, source_lang=source_lang
        )
        if translated_text is None:
            translated_text = "Translation failed"

        add_text(processed_image, translated_text, cont)

        image_info["bounding_boxes"].append(result)
        image_info["text"].append(text)
        image_info["translated_text"].append(translated_text)

    return image_info


def convert_image_to_base64(image: Image.Image) -> str:
    buff = io.BytesIO()
    image.save(buff, format="PNG")
    return base64.b64encode(buff.getvalue()).decode("utf-8")


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
def predict(request: Dict[str, Any]):
    try:
        target_lang = request["target_lang"]
        source_lang = request.get("source_lang", "ja-JP")  # Default to Japanese
        
        # Support both single image and multiple images
        images_data = request.get("images", [request.get("image")])
        if not isinstance(images_data, list):
            images_data = [images_data]
        
        results_list = []
        
        for idx, image_data in enumerate(images_data):
            # Decode and save the image
            image = decode_base64_image(image_data)
            temp_image_path = f"image_{idx}.png"
            image.save(temp_image_path)

            # Process the image
            results = predict_bounding_boxes(object_detection_model, temp_image_path)
            np_image = np.array(image)
            image_info = extract_text_from_regions(image=np_image, target_lang=target_lang, source_lang=source_lang, results=results)

            # Create result image
            result_image = Image.fromarray(np_image, "RGB")
            temp_result_path = f"translated_image_{idx}.png"
            result_image.save(temp_result_path)

            # Convert to base64
            img_str = convert_image_to_base64(result_image)

            # Clean up temporary files
            os.remove(temp_image_path)
            os.remove(temp_result_path)
            
            # Add result with index to maintain order
            results_list.append({
                "index": idx,
                "image": img_str,
                "image_info": image_info
            })

        # Return single result for backward compatibility or array for batch
        if len(results_list) == 1 and "image" in request:
            return {"image": results_list[0]["image"], "image_info": results_list[0]["image_info"]}
        else:
            return {"results": results_list}

    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Internal Server Error",
            },
        )


@app.post("/download-zip")
def download_zip(request: Dict[str, Any]):
    """Create a zip file containing all translated images"""
    try:
        images_data: List[str] = request["images"]
        
        # Create zip file in memory
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for idx, image_base64 in enumerate(images_data):
                # Decode base64 image
                image_bytes = base64.b64decode(image_base64)
                
                # Add to zip with numbered filename
                filename = f"translated_manga_{idx + 1}.png"
                zip_file.writestr(filename, image_bytes)
        
        # Seek to beginning of buffer
        zip_buffer.seek(0)
        
        # Return as streaming response
        return StreamingResponse(
            io.BytesIO(zip_buffer.read()),
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=translated_manga.zip"}
        )
        
    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Failed to create zip file",
            },
        )


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
