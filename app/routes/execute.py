from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.schemas.execute import ExecuteResult
from app.repository import execute_algorithm

import json

router = APIRouter()

@router.post("/{algorithm_key}", response_model=ExecuteResult)
async def run_algorithm(
    algorithm_key: str,
    params_json: str = Form(None),
    text: str = Form(None),
    file: UploadFile = File(None)
):
    """
    Ejecuta el algoritmo especificado con parámetros JSON, texto o imagen subida.
    """
    try:
        # Si el algoritmo es NER, construimos el params_json con el texto recibido
        if algorithm_key == "ner":
            if not text:
                raise ValueError("Se requiere un campo de texto para el algoritmo 'ner'.")
            params_json = json.dumps({"params": {"text": text}})

        result = await execute_algorithm(algorithm_key, params_json, file)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
