from fastapi import FastAPI
from app.routes import projects, files, execute

app = FastAPI()

app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(files.router, prefix="/files", tags=["files"])
app.include_router(execute.router, prefix="/execute", tags=["execute"])
