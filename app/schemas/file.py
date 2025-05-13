from pydantic import BaseModel
from typing import Literal

class FileMetaBase(BaseModel):
    name: str
    type: Literal["script", "data", "notebook", "video"]
    path: str

class FileMetaCreate(FileMetaBase):
    project_id: str

class FileMetaOut(FileMetaBase):
    id: str
    project_id: str

    class Config:
        from_attributes = True