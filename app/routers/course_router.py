from fastapi import APIRouter, Depends, status, Query, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..utils import get_db_session, get_current_user
from ..repositories import CoursesUseCases, UserUseCases, ModuleUseCases
from ..schemas import Course as CourseSchema


course_router = APIRouter(prefix="/courses")


@course_router.post("/")
def create_course(
    course_data: CourseSchema,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    course_uc = CoursesUseCases(db)
    user_uc = UserUseCases(db)
    current_user_id = user_uc.user_id_by_username(current_user["sub"])

    if course_data.professor_id != current_user_id:
        raise HTTPException(
            detail="Você só pode criar cursos para o professor autenticado.",
            status_code=status.HTTP_403_FORBIDDEN
        )

    new_course = course_uc.create_course(course_data)
    return JSONResponse(
        content=jsonable_encoder(new_course),
        status_code=status.HTTP_201_CREATED
    )

@course_router.put("/{course_id}")
def update_course(
    course_id: int,
    course_data: CourseSchema,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    course_uc = CoursesUseCases(db)
    user_uc = UserUseCases(db)
    current_user_id = user_uc.user_id_by_username(current_user["sub"])

    if course_data.professor_id != current_user_id:
        raise HTTPException(
            detail="Você só pode atualizar cursos do professor autenticado.",
            status_code=status.HTTP_403_FORBIDDEN
        )

    updated_course = course_uc.update_course(course_id, course_data)
    return JSONResponse(
        content=jsonable_encoder(updated_course),
        status_code=status.HTTP_200_OK
    )

@course_router.post("/enrollments")
def enroll_in_course(course_id: int, db: Session = Depends(get_db_session), current_user: dict = Depends(get_current_user)):
    user_uc = UserUseCases(db)
    user_uc.enroll(current_user["sub"], course_id)
    return JSONResponse(
        content={ "msg": "success" },
        status_code=status.HTTP_201_CREATED
    )

@course_router.get("/")
def list_courses(
    search: str | None = Query(default=None),
    area: str | None = Query(default=None),
    level: str | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1),
    db: Session = Depends(get_db_session)
):
    course_uc = CoursesUseCases(db)
    courses = course_uc.list_courses(
        search=search,
        area=area,
        level=level,
        page=page,
        page_size=page_size
    )
    return JSONResponse(
        content=jsonable_encoder(courses),
        status_code=status.HTTP_200_OK
    )


@course_router.get("/{course_id}")
def get_course_details(course_id: int, db: Session = Depends(get_db_session)):
    course_uc = CoursesUseCases(db)
    course = course_uc.get_course_details(course_id)
    return JSONResponse(
        content=jsonable_encoder(course),
        status_code=status.HTTP_200_OK
    )


@course_router.get("/{course_id}/modules")
def list_course_modules(course_id: int, db: Session = Depends(get_db_session)):
    module_uc = ModuleUseCases(db)
    modules = module_uc.list_by_course_id(course_id)
    return JSONResponse(
        content=jsonable_encoder(modules),
        status_code=status.HTTP_200_OK
    )

@course_router.get("/{course_id}/students")
def list_course_students(
    course_id: int,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    user_uc = UserUseCases(db)
    students = user_uc.list_students_by_course(course_id, current_user["sub"])
    return JSONResponse(
        content=jsonable_encoder(students),
        status_code=status.HTTP_200_OK
    )

@course_router.get("/professor/me/enrollments")
def get_professor_enrollment_metrics(
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    user_uc = UserUseCases(db)
    professor = user_uc.ensure_professor(current_user["sub"])
    course_uc = CoursesUseCases(db)
    metrics = course_uc.get_professor_course_enrollment_metrics(professor.id)
    return JSONResponse(
        content=jsonable_encoder(metrics),
        status_code=status.HTTP_200_OK
    )

@course_router.get("/{course_id}/quiz-metrics")
def get_course_quiz_metrics(
    course_id: int,
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    user_uc = UserUseCases(db)
    professor = user_uc.ensure_professor(current_user["sub"])
    course_uc = CoursesUseCases(db)
    metrics = course_uc.get_course_quiz_question_metrics(course_id, professor.id)
    return JSONResponse(
        content=jsonable_encoder(metrics),
        status_code=status.HTTP_200_OK
    )

@course_router.get("/students/me/progress")
def get_student_progress(
    db: Session = Depends(get_db_session),
    current_user: dict = Depends(get_current_user)
):
    user_uc = UserUseCases(db)
    progress = user_uc.get_student_course_progress(current_user["sub"])
    return JSONResponse(
        content=jsonable_encoder(progress),
        status_code=status.HTTP_200_OK
    )
