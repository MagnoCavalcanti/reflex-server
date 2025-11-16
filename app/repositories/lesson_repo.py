from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..models import Lesson as LessonModel
from ..schemas import Lesson as LessonSchema


class LessonUseCases:

    @staticmethod
    def list_all(db: Session):
        return db.query(LessonModel).all()
    @staticmethod
    def create(db: Session, data: LessonSchema):
        lesson = LessonModel(
            content_type=data.content_type,
            done=data.done,
            module_id=data.module_id
        )
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        return lesson

    @staticmethod
    def update(db: Session, lesson_id: int, data: LessonSchema):
        lesson = db.query(LessonModel).filter(LessonModel.id == lesson_id).first()

        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")

        lesson.content_type = data.content_type
        lesson.done = data.done
        lesson.module_id = data.module_id

        db.commit()
        db.refresh(lesson)
        return lesson

    @staticmethod
    def delete(db: Session, lesson_id: int):
        lesson = db.query(LessonModel).filter(LessonModel.id == lesson_id).first()

        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")

        db.delete(lesson)
        db.commit()

        return {"message": "Aula deletada com sucesso."}


