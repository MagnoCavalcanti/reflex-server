from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..models import Module as ModuleModel
from ..schemas import Module as ModuleSchema


class ModuleUseCases:

    @staticmethod
    def list_all(db: Session):
        return db.query(ModuleModel).all()

    @staticmethod
    def create(db: Session, data: ModuleSchema):
        module = ModuleModel(
            title=data.title,
            course_id=data.course_id
        )
        db.add(module)
        db.commit()
        db.refresh(module)
        return module

    @staticmethod
    def update(db: Session, module_id: int, data: ModuleSchema):
        module = db.query(ModuleModel).filter(ModuleModel.id == module_id).first()

        if not module:
            raise HTTPException(status_code=404, detail="Module not found")

        module.title = data.title
        module.course_id = data.course_id

        db.commit()
        db.refresh(module)
        return module

    @staticmethod
    def delete(db: Session, module_id: int):
        module = db.query(ModuleModel).filter(ModuleModel.id == module_id).first()

        if not module:
            raise HTTPException(status_code=404, detail="Module not found")

        db.delete(module)
        db.commit()

        return {"message": "Módulo deletado com sucesso."}


