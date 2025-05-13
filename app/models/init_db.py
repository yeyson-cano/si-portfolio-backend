# app/models/init_db.py

import asyncio
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import Base, engine, SessionLocal
from app.models.project import Project
from app.models.file import FileMeta

async def seed_data():
    async with SessionLocal() as session:  # AsyncSession
        # 1) Proyectos de ejemplo
        existing = (await session.execute(select(Project.id))).scalars().all()
        to_add_projects = []
        if "genetic-01" not in existing:
            to_add_projects.append(Project(
                id="genetic-01",
                title="Alg. Genético: VRP",
                short_desc="Optimización de rutas",
                full_desc="Implementación de un algoritmo genético para el problema de ruteo de vehículos (VRP).",
                algorithm_key="genetic"
            ))
        if "nb-01" not in existing:
            to_add_projects.append(Project(
                id="nb-01",
                title="Naive Bayes: Clasificación SMS",
                short_desc="Detección de spam en SMS",
                full_desc="Comparativa de tres variantes de Naive Bayes (Bernoulli, Multinomial, Gaussian) para clasificación de mensajes.",
                algorithm_key="nb"
            ))
        if "nn-01" not in existing:
            to_add_projects.append(Project(
                id="nn-01",
                title="Red Neuronal Manual 2-2-1",
                short_desc="Forward/backprop a mano",
                full_desc="Ejemplo práctico de cálculo manual de forward y backpropagation en red 2-2-1.",
                algorithm_key="nn"
            ))
        if to_add_projects:
            session.add_all(to_add_projects)
            await session.commit()

        # 2) Archivos de ejemplo
        existing_files = (await session.execute(select(FileMeta.id))).scalars().all()
        to_add_files = []
        # Genetic script
        if "f-g01-1" not in existing_files:
            to_add_files.append(FileMeta(
                id="f-g01-1",
                project_id="genetic-01",
                name="genetic_vrp.py",
                type="script",
                path="/data/genetic_vrp.py"
            ))
        # NB script and data
        if "f-nb01-1" not in existing_files:
            to_add_files.append(FileMeta(
                id="f-nb01-1",
                project_id="nb-01",
                name="sms_nb_comparison_with_preprocessing.py",
                type="script",
                path="/data/sms_nb_comparison_with_preprocessing.py"
            ))
        if "f-nb01-2" not in existing_files:
            to_add_files.append(FileMeta(
                id="f-nb01-2",
                project_id="nb-01",
                name="SMSSpamCollection.csv",
                type="data",
                path="/data/SMSSpamCollection.csv"
            ))
        # NN script
        if "f-nn01-1" not in existing_files:
            to_add_files.append(FileMeta(
                id="f-nn01-1",
                project_id="nn-01",
                name="nn_manual.py",
                type="script",
                path="/data/nn_manual.py"
            ))
        if to_add_files:
            session.add_all(to_add_files)
            await session.commit()

        print(f"✅ Semilla: {len(to_add_projects)} proyectos y {len(to_add_files)} archivos añadidos.")

async def init_models_and_seed():
    """
    Crea las tablas y luego inserta datos semilla si no existen.
    """
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)  # Descomenta para reset total
        await conn.run_sync(Base.metadata.create_all)
    await seed_data()

if __name__ == "__main__":
    asyncio.run(init_models_and_seed())
