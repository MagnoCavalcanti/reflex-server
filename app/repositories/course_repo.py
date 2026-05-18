from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import or_

from ..models import Course as CourseModel, User as UserModel, Module as ModuleModel, Lesson as LessonModel
from ..schemas import Course as CourseSchema

class CoursesUseCases:
    def __init__(self, db_session: Session):
        self.db = db_session

    def _serialize_course(self, course: CourseModel, professor: UserModel | None = None, include_modules: bool = False):
        if professor is None and course.professor_id:
            professor = self.db.query(UserModel).filter(UserModel.id == course.professor_id).first()

        payload = {
            "id": course.id,
            "title": course.title,
            "description": course.description,
            "area": course.area,
            "level": course.level,
            "professor_id": course.professor_id,
            "professor_name": professor.fullname if professor else None,
            "created_at": course.created_at.isoformat() if course.created_at else None,
            "updated_at": course.updated_at.isoformat() if course.updated_at else None,
        }

        if not include_modules:
            return payload

        modules = self.db.query(ModuleModel).filter(ModuleModel.course_id == course.id).all()
        modules_payload = []
        for module in modules:
            lessons = self.db.query(LessonModel).filter(LessonModel.module_id == module.id).all()
            modules_payload.append(
                {
                    "id": module.id,
                    "title": module.title,
                    "lessons": [
                        {
                            "id": lesson.id,
                            "title": lesson.title,
                            "content_type": lesson.content_type
                        }
                        for lesson in lessons
                    ]
                }
            )

        payload["modules"] = modules_payload
        return payload

    
    def list_courses(
        self,
        search: str | None = None,
        area: str | None = None,
        level: str | None = None,
        page: int = 1,
        page_size: int = 20
    ):
        query = self.db.query(CourseModel)

        if search:
            search_term = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    CourseModel.title.ilike(search_term),
                    CourseModel.description.ilike(search_term)
                )
            )

        if area:
            query = query.filter(CourseModel.area.ilike(area.strip()))

        if level:
            query = query.filter(CourseModel.level.ilike(level.strip()))

        total = query.count()

        courses = (
            query
            .offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        if not courses:
            return {
                "total": total,
                "page": page,
                "page_size": page_size,
                "results": []
            }

        professor_ids = {course.professor_id for course in courses if course.professor_id}
        professors = self.db.query(UserModel).filter(UserModel.id.in_(professor_ids)).all() if professor_ids else []
        professor_by_id = {professor.id: professor for professor in professors}

        results = [
            self._serialize_course(course, professor=professor_by_id.get(course.professor_id), include_modules=False)
            for course in courses
        ]

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "results": results
        }

    def get_course_details(self, course_id: int):
        course = self.db.query(CourseModel).filter(CourseModel.id == course_id).first()
        if not course:
            raise HTTPException(
                detail="Curso não encontrado",
                status_code=status.HTTP_404_NOT_FOUND
            )

        professor = self.db.query(UserModel).filter(UserModel.id == course.professor_id).first()
        return self._serialize_course(course, professor=professor, include_modules=True)
    
    def create_course(self, course_data: CourseSchema):

        professor = course_data.professor_id
        user = self.db.query(UserModel).filter(
            UserModel.id == professor,
            UserModel.type_user == "P"
        ).first()
        if not user:
            raise HTTPException(detail="Professor não encontrado ou inválido.", status_code=status.HTTP_404_NOT_FOUND)
        new_course = CourseModel(**course_data.__dict__)
        
        try:
            self.db.add(new_course)
            self.db.commit()
            self.db.refresh(new_course)
            return self._serialize_course(new_course, professor=user, include_modules=False)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(detail="Erro ao criar o curso.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)