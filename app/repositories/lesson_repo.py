from sqlalchemy.orm import Session
from fastapi import HTTPException

from ..models.models import Lesson
from ..schemas.Lesson import LessonCreate, LessonUpdate


class LessonRepository:

    @staticmethod
    def list_all(db: Session):
        return db.query(Lesson).all()

    @staticmethod
    def create(db: Session, data: LessonCreate):
        lesson = Lesson(
            content_type=data.content_type,
            done=data.done,
            module_id=data.module_id
        )
        db.add(lesson)
        db.commit()
        db.refresh(lesson)
        return lesson

    @staticmethod
    def update(db: Session, lesson_id: int, data: LessonUpdate):
        lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()

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
        lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()

        if not lesson:
            raise HTTPException(status_code=404, detail="Lesson not found")

        db.delete(lesson)
        db.commit()

        return {"message": "Aula deletada com sucesso."}


