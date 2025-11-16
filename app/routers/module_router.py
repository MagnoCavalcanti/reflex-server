from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.utils import get_db_session
from app.repositories.module_repo import ModuleUseCases
from app.schemas import Module as ModuleSchema

module_router = APIRouter(prefix="/modules")

@module_router.get("/")
def list_modules(db: Session = Depends(get_db_session)):
    module_uc = ModuleUseCases(db)
    modules = module_uc.list_all()
    return JSONResponse(
        content=modules,
        status_code=status.HTTP_200_OK
    )

@module_router.post("/")
def create_module(module: ModuleSchema, db: Session = Depends(get_db_session)):
    module_uc = ModuleUseCases(db)
    module_uc.create(module)
    return JSONResponse(
        content={ "msg": "success" },
        status_code=status.HTTP_201_CREATED
    )





