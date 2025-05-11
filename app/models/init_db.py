import asyncio
from app.db import Base, engine

async def init_models():
    """
    Crea las tablas definidas en Base.metadata.
    Ejecuta: python -m app.models.init_db
    """
    async with engine.begin() as conn:
        # Para resetear tablas existentes, descomenta la siguiente línea:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tablas creadas correctamente.")

if __name__ == "__main__":
    asyncio.run(init_models())
