from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.utils.dependencies import get_db_session
from app.repositories.lesson_repo import LessonUseCases
from app.schemas import Lesson as LessonSchema

lesson_router = APIRouter(prefix="/lessons")

@lesson_router.get("/")
def list_lessons(db: Session = Depends(get_db_session)):
    return LessonUseCases.list_all(db)

@lesson_router.post("/")
def create_lesson(lesson: LessonSchema, db: Session = Depends(get_db_session)):
    return LessonUseCases.create(db, lesson)

@lesson_router.put("/{lesson_id}")
def update_lesson(lesson_id: int, data: LessonSchema, db: Session = Depends(get_db_session)):
    return LessonUseCases.update(db, lesson_id, data)

@lesson_router.delete("/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db_session)):
    return LessonUseCases.delete(db, lesson_id)

