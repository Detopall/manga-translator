import os
import io
import base64
from typing import Dict, Any

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

from utils.predict_bounding_boxes import predict_bounding_boxes
from utils.manga_ocr_utils import get_text_from_image
from utils.translate_manga import translate_manga
from utils.process_contour import process_contour
from utils.write_text_on_image import add_text

MODEL_PATH = "./model_creation/runs/detect/train5/weights/best.pt"
object_detection_model = YOLO(MODEL_PATH)

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
    image: np.ndarray, target_lang: str, results: list
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
            text, target_lang=target_lang, source_lang="ja-JP"
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
        image = decode_base64_image(request["image"])
        image.save("image.png")

        target_lang = request["target_lang"]

        results = predict_bounding_boxes(object_detection_model, "image.png")
        np_image = np.array(image)
        image_info = extract_text_from_regions(np_image, target_lang, results)

        result_image = Image.fromarray(np_image, "RGB")
        result_image.save("translated_image.png")

        img_str = convert_image_to_base64(result_image)

        os.remove("image.png")
        os.remove("translated_image.png")

        return {"image": img_str, "image_info": image_info}

    except Exception as e:
        print(e)
        return JSONResponse(
            status_code=500,
            content={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": "Internal Server Error",
            },
        )


if __name__ == "__main__":
    uvicorn.run("app:app", host="localhost", port=8000, reload=True)
