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

        modules = self.db.query(ModuleModel).filter(ModuleModel.course_id == course_id).all()
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
    
    

    def create(self, data: ModuleSchema, username: int):
        try:

            user_id = self.db.query(UserModel.id).filter(UserModel.username == username).scalar()
            
            # Verificar se o curso existe
            course = self.db.query(CourseModel).filter(CourseModel.id == data.course_id).first()
            if not course:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")
            
            # Verificar se o usuário é o professor do curso
            if course.professor_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, 
                    detail="Apenas o professor do curso pode criar módulos"
                )
            
            module = ModuleModel(**data.__dict__)
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
        

    


