import os
from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import SessionLocal
from app.models.project import Project
from app.models.file import FileMeta
from app.schemas.project import ProjectOut
from app.schemas.file import FileMetaOut
from app.schemas.execute import (
    ExecuteParams,
    ExecuteResult,
    EpochStats,
    FirstEpochOut,
)

# Funciones de algoritmos
from app.algorithms.genetic import run_genetic
from app.algorithms.nb import run_naive_bayes
from app.algorithms.nn import run_nn_manual
from app.algorithms.vision import run_vision_image  # <- asegúrate de tenerlo

from fastapi import UploadFile
import json

async def get_projects() -> List[ProjectOut]:
    async with SessionLocal() as session:
        result = await session.execute(select(Project))
        projects = result.scalars().all()

    projects_out: List[ProjectOut] = []
    for proj in projects:
        files = await get_files_for_project(proj.id)
        proj_out = ProjectOut.from_orm(proj)
        proj_out.files = files
        projects_out.append(proj_out)

    return projects_out

async def get_project(project_id: str) -> ProjectOut:
    async with SessionLocal() as session:
        proj: Optional[Project] = await session.get(Project, project_id)
    if proj is None:
        raise ValueError(f"Project with id '{project_id}' not found")

    files = await get_files_for_project(project_id)
    proj_out = ProjectOut.from_orm(proj)
    proj_out.files = files
    return proj_out

async def get_files_for_project(project_id: str) -> List[FileMetaOut]:
    async with SessionLocal() as session:
        result = await session.execute(
            select(FileMeta).where(FileMeta.project_id == project_id)
        )
        files = result.scalars().all()
    return [FileMetaOut.from_orm(f) for f in files]

async def get_file(file_id: str) -> FileMetaOut:
    async with SessionLocal() as session:
        file_obj: Optional[FileMeta] = await session.get(FileMeta, file_id)
    if file_obj is None:
        raise ValueError(f"File with id '{file_id}' not found")
    return FileMetaOut.from_orm(file_obj)

# 🚨 Este es el que cambia
async def execute_algorithm(
    algorithm_key: str,
    params_json: Optional[str] = None,
    file: Optional[UploadFile] = None
) -> ExecuteResult:
    """
    Ejecuta el algoritmo correspondiente según `algorithm_key`.
    """
    if algorithm_key == "genetic":
        params = ExecuteParams(**json.loads(params_json))
        raw = run_genetic(params.params, params.verbosity)

    elif algorithm_key == "nb":
        params = ExecuteParams(**json.loads(params_json))
        raw = run_naive_bayes(params.params, params.verbosity)

    elif algorithm_key == "nn":
        params = ExecuteParams(**json.loads(params_json))
        raw = run_nn_manual(params.params, params.verbosity)

    elif algorithm_key == "vision":
        if not file:
            raise ValueError("Se requiere un archivo de imagen para el algoritmo de visión.")
        raw = run_vision_image(file)

    else:
        raise ValueError(f"Unknown algorithm key: {algorithm_key}")

    return ExecuteResult(**raw)
