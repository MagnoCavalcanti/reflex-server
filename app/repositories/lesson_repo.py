from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models import Lesson as LessonModel, Module as ModuleModel, Course as CourseModel, User as UserModel
from ..schemas import Lesson as LessonSchema


class LessonUseCases:

    def __init__(self, db_session: Session):
        self.db = db_session

    def list_all(self):
        return self.db.query(LessonModel).all()

    def create(self, data: LessonSchema, username: str):
        try:
            # Buscar o ID do usuário
            user_id = self.db.query(UserModel.id).filter(UserModel.username == username).scalar()
            
            # Verificar se o módulo existe
            module = self.db.query(ModuleModel).filter(ModuleModel.id == data.module_id).first()
            if not module:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Módulo não encontrado")
            
            # Verificar se o curso existe
            course = self.db.query(CourseModel).filter(CourseModel.id == module.course_id).first()
            if not course:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")
            
            # Verificar se o usuário é o professor do curso
            if course.professor_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, 
                    detail="Apenas o professor do curso pode criar aulas"
                )
            
            lesson = LessonModel(**data.__dict__)
            self.db.add(lesson)
            self.db.commit()
            self.db.refresh(lesson)
            return lesson
        except HTTPException:
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar aula")

    

