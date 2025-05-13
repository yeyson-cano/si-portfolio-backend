from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.routes import projects, files, execute

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/data", StaticFiles(directory="/data"), name="data")

app.include_router(projects.router, prefix="/projects", tags=["projects"])
app.include_router(files.router, prefix="/files", tags=["files"])
app.include_router(execute.router, prefix="/execute", tags=["execute"])
