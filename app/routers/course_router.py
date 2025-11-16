from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..utils import get_db_session, get_current_user
from ..repositories import CoursesUseCases, UserUseCases
from ..schemas import Course as CourseSchema


course_router = APIRouter(prefix="/courses")

@course_router.get("/")
def list_courses(db: Session = Depends(get_db_session)):
    course_uc = CoursesUseCases(db)
    courses = course_uc.list_courses()
    return JSONResponse(
        content=jsonable_encoder(courses),
        status_code=status.HTTP_200_OK
    )

@course_router.post("/")
def create_course(course_data: CourseSchema, db: Session = Depends(get_db_session)):
    course_uc = CoursesUseCases(db)
    new_course = course_uc.create_course(course_data)
    return JSONResponse(
        content={"message": "Curso criado com sucesso."},
        status_code=status.HTTP_201_CREATED
    )

@course_router.post("/enrollments")
def enroll_in_course(course_id: int, db: Session = Depends(get_db_session), current_user: dict = Depends(get_current_user)):
    user_uc = UserUseCases(db)
    user_uc.enroll(current_user["sub"], course_id)
    return JSONResponse(
        content={ "msg": "success" },
        status_code=status.HTTP_201_CREATED
    )
