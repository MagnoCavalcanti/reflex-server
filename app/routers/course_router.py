from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..utils import get_db_session 
from ..repositories.course_repo import CoursesUseCases
from ..schemas import Course as CourseSchema


course_router = APIRouter(prefix="/courses")

@course_router.get("/")
def list_courses(db: Session = Depends(get_db_session)):
    course_uc = CoursesUseCases(db)
    courses = course_uc.list_courses()
    return JSONResponse(
        content=courses,
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

