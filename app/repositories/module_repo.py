from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models import Module as ModuleModel
from ..schemas import Module as ModuleSchema


class ModuleUseCases:

    def __init__(self, db_session: Session):
        self.db = db_session

    def list_all(self):
        return self.db.query(ModuleModel).all()

    def create(self, data: ModuleSchema):
        try:
            module = ModuleModel(**data.__dict__)
            self.db.add(module)
            self.db.commit()
            self.db.refresh(module)
            return module
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar módulo")
        

    


