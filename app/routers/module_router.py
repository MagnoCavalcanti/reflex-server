from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.utils import get_db_session
from app.repositories.module_repo import ModuleUseCases
from app.schemas import Module as ModuleSchema

module_router = APIRouter(prefix="/modules")

@module_router.get("/")
def list_modules(db: Session = Depends(get_db_session)):
    return ModuleUseCases.list_all(db)

@module_router.post("/")
def create_module(module: ModuleSchema, db: Session = Depends(get_db_session)):
    return ModuleUseCases.create(db, module)

@module_router.put("/{module_id}")
def update_module(module_id: int, data: ModuleSchema, db: Session = Depends(get_db_session)):
    return ModuleUseCases.update(db, module_id, data)

@module_router.delete("/{module_id}")
def delete_module(module_id: int, db: Session = Depends(get_db_session)):
    return ModuleUseCases.delete(db, module_id)



