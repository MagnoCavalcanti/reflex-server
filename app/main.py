from fastapi import FastAPI, Depends

from .utils import get_current_user
from .routers import auth_router, course_router
from app.routers.module_router import router as module_router
from app.routers.lesson_router import router as lesson_router



app = FastAPI()

@app.get("/")
def home():
    return {
        "mensage": "Inittial Project"
    }


app.include_router(auth_router)
app.include_router(course_router)
app.include_router(module_router)
app.include_router(lesson_router)

