from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.schemas.execute import ExecuteResult
from app.repository import execute_algorithm

router = APIRouter()

@router.post("/{algorithm_key}", response_model=ExecuteResult)
async def run_algorithm(
    algorithm_key: str,
    params_json: str = Form(None),
    file: UploadFile = File(None)
):
    """
    Ejecuta el algoritmo especificado con parámetros JSON o imagen subida.
    """
    try:
        result = await execute_algorithm(algorithm_key, params_json, file)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
