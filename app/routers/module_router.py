from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.utils.dependencies import get_db_session
from app.repositories.module_repo import ModuleRepository
from app.schemas.Module import ModuleCreate, ModuleResponse, ModuleUpdate

router = APIRouter(
    prefix="/modules",
    tags=["modules"]
)

@router.get("/", response_model=List[ModuleResponse])
def list_modules(db: Session = Depends(get_db_session)):
    return ModuleRepository.list_all(db)

@router.post("/", response_model=ModuleResponse)
def create_module(module: ModuleCreate, db: Session = Depends(get_db_session)):
    return ModuleRepository.create(db, module)

@router.put("/{module_id}", response_model=ModuleResponse)
def update_module(module_id: int, data: ModuleUpdate, db: Session = Depends(get_db_session)):
    return ModuleRepository.update(db, module_id, data)

@router.delete("/{module_id}")
def delete_module(module_id: int, db: Session = Depends(get_db_session)):
    return ModuleRepository.delete(db, module_id)



