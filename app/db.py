import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexión a PostgreSQL (ajusta usuario, contraseña, host, puerto y nombre de BD)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://si_user:si_password_segura@db/si_portfolio"
)
# Creamos el engine asíncrono
engine = create_async_engine(
    DATABASE_URL,
    echo=True,               # Muestra las consultas SQL en consola para debugging
    future=True,             # Usa la API 2.0 de SQLAlchemy
)

# Definimos la fábrica de sesiones asíncronas
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Evita expirar atributos al hacer commit
)

# Base declarativa para los modelos
Base = declarative_base()
