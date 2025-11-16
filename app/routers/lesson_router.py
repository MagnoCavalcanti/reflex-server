from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.utils.dependencies import get_db_session, get_current_user
from app.repositories.lesson_repo import LessonUseCases
from app.schemas import Lesson as LessonSchema

lesson_router = APIRouter(prefix="/lessons")

@lesson_router.get("/")
def list_lessons(db: Session = Depends(get_db_session)):
    lesson_uc = LessonUseCases(db)
    lessons = lesson_uc.list_all()
    return JSONResponse(
        content=lessons,
        status_code=status.HTTP_200_OK
    )

@lesson_router.post("/")
def create_lesson(
    lesson: LessonSchema, 
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    lesson_uc = LessonUseCases(db)
    lesson_uc.create(lesson, current_user["sub"])
    return JSONResponse(
        content={ "msg": "success" },
        status_code=status.HTTP_201_CREATED
    )



