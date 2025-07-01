from transformers import AutoTokenizer, AutoModelForTokenClassification
import os

model_name = "dslim/bert-base-NER"
cache_dir = "saved_models/ner_model/"

# Solo descarga si aún no existe
if not os.path.exists(cache_dir):
    print("🔄 Descargando modelo NER...")
    AutoTokenizer.from_pretrained(model_name, cache_dir=cache_dir)
    AutoModelForTokenClassification.from_pretrained(model_name, cache_dir=cache_dir)
    print("✅ Descarga completada.")
else:
    print("✅ Modelo NER ya está presente.")
