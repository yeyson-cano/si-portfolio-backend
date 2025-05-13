from pydantic import BaseModel
from typing import Optional, List
from app.schemas.file import FileMetaOut

class ProjectBase(BaseModel):
    title: str
    short_desc: str
    full_desc: Optional[str] = None
    algorithm_key: str

class ProjectCreate(ProjectBase):
    """Esquema para crear un proyecto (si se necesitara)."""
    pass

class ProjectOut(ProjectBase):
    id: str
    files: List[FileMetaOut] = []

    class Config:
        from_attributes = True
