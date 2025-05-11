from sqlalchemy import Column, String, Text
from app.db import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    short_desc = Column(String, nullable=False)
    full_desc = Column(Text, nullable=True)
    algorithm_key = Column(String, nullable=False)
