from fastapi import FastAPI, Depends

from .utils import get_current_user
from .routers import auth_router, course_router
from app.routers import module_router
from app.routers import lesson_router



app = FastAPI()

@app.get("/")
def home():
    return {
        "mensage": "Inittial Project"
    }


app.include_router(auth_router, tags=["auth"])
app.include_router(course_router, tags=["courses"], dependencies=[Depends(get_current_user)])
app.include_router(module_router, tags=["modules"], dependencies=[Depends(get_current_user)])
app.include_router(lesson_router, tags=["lessons"], dependencies=[Depends(get_current_user)])

