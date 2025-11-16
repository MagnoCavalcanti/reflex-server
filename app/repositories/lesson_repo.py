from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..models import Lesson as LessonModel
from ..schemas import Lesson as LessonSchema


class LessonUseCases:

    def __init__(self, db_session: Session):
        self.db = db_session

    def list_all(self):
        return self.db.query(LessonModel).all()

    def create(self, data: LessonSchema):
        try:
            lesson = LessonModel(**data.__dict__)
            self.db.add(lesson)
            self.db.commit()
            self.db.refresh(lesson)
            return lesson
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="Erro ao criar aula")

    

