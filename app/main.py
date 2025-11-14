from fastapi import FastAPI, Depends

from .utils import get_current_user
from .routers import auth_router, course_router

app = FastAPI()

@app.get("/")
def home():
    return {
        "mensage": "Inittial Project"
    }


app.include_router(auth_router)
app.include_router(course_router)