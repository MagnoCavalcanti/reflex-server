from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.utils import get_db_session, get_current_user
from app.repositories import ModuleUseCases, UserUseCases
from app.schemas import Module as ModuleSchema

module_router = APIRouter(prefix="/modules")

@module_router.get("/")
def list_modules(db: Session = Depends(get_db_session)):
    module_uc = ModuleUseCases(db)
    modules = module_uc.list_all()
    return JSONResponse(
        content=jsonable_encoder(modules),
        status_code=status.HTTP_200_OK
    )

@module_router.post("/")
def create_module(
    module: ModuleSchema, 
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    module_uc = ModuleUseCases(db)
    print(current_user)
    module_uc.create(module, current_user["sub"])
    return JSONResponse(
        content={ "msg": "success" },
        status_code=status.HTTP_201_CREATED
    )

@module_router.get("/{module_id}")
def get_module(module_id: int, db: Session = Depends(get_db_session)):
    module_uc = ModuleUseCases(db)
    module = module_uc.get_by_id(module_id)
    return JSONResponse(
        content=jsonable_encoder(module),
        status_code=status.HTTP_200_OK
    )

@module_router.post("/{module_id}")
def complete_module(
    module_id: int,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    user_uc = UserUseCases(db)
    user_uc.complete_module(current_user["sub"], module_id)
    return JSONResponse(
        content={ "msg": "success" },
        status_code=status.HTTP_200_OK
    )
