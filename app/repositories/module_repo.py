from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models import Module as ModuleModel, User as UserModel, Course as CourseModel, Lesson as LessonModel
from ..schemas import Module as ModuleSchema


class ModuleUseCases:

    def __init__(self, db_session: Session):
        self.db = db_session

    def list_all(self):
        return self.db.query(ModuleModel).all()

    def list_by_course_id(self, course_id: int):
        course = self.db.query(CourseModel).filter(CourseModel.id == course_id).first()
        if not course:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Curso não encontrado"
            )

        modules = (
            self.db.query(ModuleModel)
            .filter(ModuleModel.course_id == course_id)
            .order_by(ModuleModel.order_index.asc(), ModuleModel.id.asc())
            .all()
        )
        if not modules:
            return []

        payload = []
        for module in modules:
            lessons = self.db.query(LessonModel).filter(LessonModel.module_id == module.id).all()
            payload.append(
                {
                    "id": module.id,
                    "title": module.title,
                    "course_id": module.course_id,
                    "order_index": module.order_index,
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
        return payload
    
    def get_by_id(self, module_id: int):
            module = self.db.query(ModuleModel).filter(ModuleModel.id == module_id).first()
            if not module:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Módulo não encontrado")
            return module

    def _require_course_owner(self, course_id: int, username: str):
        user_id = self.db.query(UserModel.id).filter(UserModel.username == username).scalar()
        course = self.db.query(CourseModel).filter(CourseModel.id == course_id).first()
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")
        if course.professor_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Apenas o professor do curso pode criar módulos"
            )
        return course

    def create(self, data: ModuleSchema, username: str):
        try:
            self._require_course_owner(data.course_id, username)
            next_order = data.order_index
            if next_order is None:
                max_order = (
                    self.db.query(ModuleModel.order_index)
                    .filter(ModuleModel.course_id == data.course_id)
                    .order_by(ModuleModel.order_index.desc())
                    .scalar()
                )
                next_order = (max_order + 1) if max_order is not None else 1

            module = ModuleModel(
                title=data.title,
                course_id=data.course_id,
                order_index=next_order
            )
            self.db.add(module)
            self.db.commit()
            self.db.refresh(module)
            return module
        except HTTPException:
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar módulo")
        

    


