from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.utils.dependencies import get_db_session
from app.repositories.lesson_repo import LessonRepository
from app.schemas.Lesson import LessonCreate, LessonResponse, LessonUpdate

router = APIRouter(
    prefix="/lessons",
    tags=["lessons"]
)

@router.get("/", response_model=List[LessonResponse])
def list_lessons(db: Session = Depends(get_db_session)):
    return LessonRepository.list_all(db)

@router.post("/", response_model=LessonResponse)
def create_lesson(lesson: LessonCreate, db: Session = Depends(get_db_session)):
    return LessonRepository.create(db, lesson)

@router.put("/{lesson_id}", response_model=LessonResponse)
def update_lesson(lesson_id: int, data: LessonUpdate, db: Session = Depends(get_db_session)):
    return LessonRepository.update(db, lesson_id, data)

@router.delete("/{lesson_id}")
def delete_lesson(lesson_id: int, db: Session = Depends(get_db_session)):
    return LessonRepository.delete(db, lesson_id)

