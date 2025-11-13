from fastapi import FastAPI

from .routers import auth_router

app = FastAPI()

@app.get("/")
def home():
    return {
        "mensage": "Inittial Project"
    }


app.include_router(auth_router)