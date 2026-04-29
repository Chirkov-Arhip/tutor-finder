from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from src.api.auth import router as auth_router
from src.api.students import router as students_router
from src.api.tutors import router as tutors_router

app = FastAPI(
    title="TutorFinder API",
    description="API для онлайн-подбора репетиторов",
    version="0.1.0"
)

app.include_router(auth_router, prefix="/api/auth", tags=["Auth"])
app.include_router(students_router, prefix="/api/students", tags=["Students"])
app.include_router(tutors_router, prefix="/api/tutors", tags=["Tutors"])

app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")

import uvicorn

def start():
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080)

def dev():
    uvicorn.run("src.main:app", host="0.0.0.0", port=8080, reload=True)