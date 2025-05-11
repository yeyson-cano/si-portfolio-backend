from fastapi import APIRouter, HTTPException
from typing import List

from app.repository import get_projects, get_project
from app.schemas.project import ProjectOut

router = APIRouter()


@router.get("/", response_model=List[ProjectOut])
async def list_projects():
    """
    Devuelve el listado de todos los proyectos.
    """
    return await get_projects()


@router.get("/{project_id}", response_model=ProjectOut)
async def retrieve_project(project_id: str):
    """
    Devuelve los datos de un único proyecto.
    """
    try:
        return await get_project(project_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
