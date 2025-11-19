from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from app.utils.dependencies import get_db_session, get_current_user
from app.repositories import LessonUseCases, UserUseCases
from app.schemas import Lesson as LessonSchema, LessonVideo as LessonVideoSchema, LessonQuiz as LessonQuizSchema, QuizQuestion as QuizQuestionSchema

lesson_router = APIRouter(prefix="/lessons")

@lesson_router.get("/")
def list_lessons(db: Session = Depends(get_db_session)):
    lesson_uc = LessonUseCases(db)
    lessons = lesson_uc.list_all()
    return JSONResponse(
        content=jsonable_encoder(lessons),
        status_code=status.HTTP_200_OK
    )

@lesson_router.post("/")
def create_lesson(
    lesson: LessonSchema, 
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    lesson_uc = LessonUseCases(db)
    new_lesson = lesson_uc.create(lesson, current_user["sub"])
    return JSONResponse(
        content={ "msg": "success", "id": new_lesson.id },
        status_code=status.HTTP_201_CREATED
    )

@lesson_router.get("/{lesson_id}")
def get_lesson(lesson_id: int, db: Session = Depends(get_db_session)):
    lesson_uc = LessonUseCases(db)
    lesson = lesson_uc.get_by_id(lesson_id)
    return JSONResponse(
        content=jsonable_encoder(lesson),
        status_code=status.HTTP_200_OK
    )

@lesson_router.post("/{lesson_id}")
def complete_lesson(
    lesson_id: int,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    user_uc = UserUseCases(db)
    user_uc.complete_lesson(current_user["sub"], lesson_id)
    return JSONResponse(
        content={ "msg": "success" },
        status_code=status.HTTP_200_OK
    )

@lesson_router.post("/create/video")
def create_lesson_video(
    lesson: LessonVideoSchema, 
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    lesson_uc = LessonUseCases(db)
    lesson_uc.create_video(lesson, current_user["sub"])
    return JSONResponse(
        content={ "msg": "success" },
        status_code=status.HTTP_201_CREATED
    )

@lesson_router.post("/create/quiz")
def create_lesson_quiz(
    lesson: LessonQuizSchema, 
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    lesson_uc = LessonUseCases(db)
    lesson_uc.create_quiz(lesson, current_user["sub"])
    return JSONResponse(
        content={ "msg": "success" },
        status_code=status.HTTP_201_CREATED
    )

@lesson_router.get("/quiz/questions")
def get_quiz_questions(quiz_id: int, db: Session = Depends(get_db_session)):
    lesson_uc = LessonUseCases(db)
    questions = lesson_uc.get_quiz_questions(quiz_id)
    return JSONResponse(
        content=jsonable_encoder(questions),
        status_code=status.HTTP_200_OK
    )

@lesson_router.post("/quiz/question")
def add_question_to_quiz(
    question: QuizQuestionSchema,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    lesson_uc = LessonUseCases(db)
    lesson_uc.add_question_to_quiz(question, current_user["sub"])
    return JSONResponse(
        content={ "msg": "success" },
        status_code=status.HTTP_201_CREATED
    )

@lesson_router.post("/quiz/answer")
def answer_quiz(
    lesson_id: int,
    quiz_id: int,
    answer_option_ids: list[int],
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    user_uc = UserUseCases(db)
    user_uc.answer_quiz(current_user["sub"], quiz_id, answer_option_ids)
    user_uc.complete_lesson(current_user["sub"], lesson_id=lesson_id)
    return JSONResponse(
        content={ "msg": "success" },
        status_code=status.HTTP_200_OK
    )


