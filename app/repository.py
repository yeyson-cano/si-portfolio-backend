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

# Importa aquí tus funciones de ejecución de algoritmos.
# Asegúrate de implementarlas en los módulos correspondientes.
from app.algorithms.genetic import run_genetic
from app.algorithms.nb import run_naive_bayes
from app.algorithms.nn import run_nn_manual


async def get_projects() -> List[ProjectOut]:
    """
    Devuelve todos los proyectos con su metadata y archivos asociados.
    """
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
    """
    Devuelve un único proyecto (o lanza ValueError si no existe).
    """
    async with SessionLocal() as session:
        proj: Optional[Project] = await session.get(Project, project_id)
    if proj is None:
        raise ValueError(f"Project with id '{project_id}' not found")

    files = await get_files_for_project(project_id)
    proj_out = ProjectOut.from_orm(proj)
    proj_out.files = files
    return proj_out


async def get_files_for_project(project_id: str) -> List[FileMetaOut]:
    """
    Lista todos los archivos asociados a un proyecto.
    """
    async with SessionLocal() as session:
        result = await session.execute(
            select(FileMeta).where(FileMeta.project_id == project_id)
        )
        files = result.scalars().all()
    return [FileMetaOut.from_orm(f) for f in files]


async def get_file(file_id: str) -> FileMetaOut:
    """
    Devuelve la metadata de un archivo (o lanza ValueError si no existe).
    """
    async with SessionLocal() as session:
        file_obj: Optional[FileMeta] = await session.get(FileMeta, file_id)
    if file_obj is None:
        raise ValueError(f"File with id '{file_id}' not found")
    return FileMetaOut.from_orm(file_obj)


async def execute_algorithm(
    algorithm_key: str, params: ExecuteParams
) -> ExecuteResult:
    """
    Llama al microservicio correspondiente según `algorithm_key`
    y convierte su salida directamente en ExecuteResult.
    """
    # 1. Ejecutar el algoritmo adecuado
    if algorithm_key == "genetic":
        raw = run_genetic(params.params, params.verbosity)
    elif algorithm_key == "nb":
        raw = run_naive_bayes(params.params, params.verbosity)
    elif algorithm_key == "nn":
        raw = run_nn_manual(params.params, params.verbosity)
    else:
        raise ValueError(f"Unknown algorithm key: {algorithm_key}")

    # 2. Pasa todo el diccionario crudo a Pydantic
    #    ExecuteResult tiene: history, first_epoch, final (Union[FinalOutGenetic, FinalOutNB])
    return ExecuteResult(**raw)
