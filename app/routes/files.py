from fastapi import APIRouter, HTTPException
from typing import List

from app.repository import get_files_for_project, get_file
from app.schemas.file import FileMetaOut

router = APIRouter()


@router.get("/projects/{project_id}/files", response_model=List[FileMetaOut])
async def list_files_for_project(project_id: str):
    """
    Lista todos los archivos asociados a un proyecto dado.
    """
    try:
        return await get_files_for_project(project_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{file_id}", response_model=FileMetaOut)
async def retrieve_file(file_id: str):
    """
    Devuelve la metadata de un archivo específico.
    """
    try:
        return await get_file(file_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
