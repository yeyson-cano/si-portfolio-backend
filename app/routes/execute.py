from fastapi import APIRouter, HTTPException
from app.schemas.execute import ExecuteParams, ExecuteResult
from app.repository import execute_algorithm

router = APIRouter()


@router.post("/{algorithm_key}", response_model=ExecuteResult)
async def run_algorithm(algorithm_key: str, params: ExecuteParams):
    """
    Ejecuta el algoritmo especificado con los parámetros dados.
    """
    try:
        result = await execute_algorithm(algorithm_key, params)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
