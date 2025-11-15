from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..models.models import Module, Course
from ..schemas.Module import ModuleCreate, ModuleUpdate


class ModuleRepository:

    @staticmethod
    def list_all(db: Session):
        return db.query(Module).all()

    @staticmethod
    def create(db: Session, data: ModuleCreate):
        module = Module(
            title=data.title,
            course_id=data.course_id
        )
        db.add(module)
        db.commit()
        db.refresh(module)
        return module

    @staticmethod
    def update(db: Session, module_id: int, data: ModuleUpdate):
        module = db.query(Module).filter(Module.id == module_id).first()

        if not module:
            raise HTTPException(status_code=404, detail="Module not found")

        module.title = data.title
        module.course_id = data.course_id

        db.commit()
        db.refresh(module)
        return module

    @staticmethod
    def delete(db: Session, module_id: int):
        module = db.query(Module).filter(Module.id == module_id).first()

        if not module:
            raise HTTPException(status_code=404, detail="Module not found")

        db.delete(module)
        db.commit()

        return {"message": "Módulo deletado com sucesso."}


