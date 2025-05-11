from sqlalchemy import Column, String, ForeignKey
from app.db import Base

class FileMeta(Base):
    __tablename__ = "files"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)   # "script", "data", "notebook", "video"
    path = Column(String, nullable=False)   # ruta en disco o URL
