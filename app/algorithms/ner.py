from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from app.schemas.execute import FinalOutNER

# Ruta al modelo local (caché)
MODEL_NAME = "dslim/bert-base-NER"
CACHE_DIR = "saved_models/ner_model"

# Cargar modelo y tokenizer desde caché local (si está disponible)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, cache_dir=CACHE_DIR)
model = AutoModelForTokenClassification.from_pretrained(MODEL_NAME, cache_dir=CACHE_DIR)

# Crear pipeline de reconocimiento de entidades
nlp = pipeline("ner", model=model, tokenizer=tokenizer, grouped_entities=True)

def run_ner_text(text: str, verbosity: str = "final") -> dict:
    """
    Ejecuta el análisis NER sobre el texto dado.
    """
    input_text = text.strip()
    if not input_text:
        raise ValueError("No se proporcionó texto para analizar.")

    ner_results = nlp(input_text)

    # Convertir resultados en forma estructurada
    entities = [
        {
            "text": ent["word"],
            "label": ent["entity_group"],
            "score": round(float(ent["score"]), 4)
        }
        for ent in ner_results
    ]

    return {
        "history": [],
        "first_epoch": None,
        "final": {
            "entities": entities
        }
    }
