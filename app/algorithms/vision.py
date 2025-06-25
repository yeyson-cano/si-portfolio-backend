import tensorflow as tf
import numpy as np
from fastapi import UploadFile
from PIL import Image
import io

MODEL_PATH = "saved_models/flower_classifier_model.keras"
CLASS_NAMES = ['daisy', 'dandelion', 'roses', 'sunflowers', 'tulips']

# Carga el modelo solo una vez
model = tf.keras.models.load_model(MODEL_PATH)

def preprocess_image(image_bytes) -> np.ndarray:
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    image = image.resize((224, 224))
    img_array = tf.keras.utils.img_to_array(image)
    img_array = tf.expand_dims(img_array, 0)
    return img_array / 255.0

def run_vision_image(file: UploadFile) -> dict:
    image_bytes = file.file.read()
    processed_image = preprocess_image(image_bytes)

    predictions = model.predict(processed_image)
    predicted_index = np.argmax(predictions[0])
    predicted_class = CLASS_NAMES[predicted_index]
    confidence = float(predictions[0][predicted_index])

    return {
        "history": [
            {
                "gen": 0,
                "best": None,
                "avg": None
            }
        ],
        "first_epoch": {
            "best": None,
            "avg": None,
            "population": []
        },
        "final": {
            "type": "vision",
            "prediction": predicted_class,
            "confidence": round(confidence, 4)
        }
    }
