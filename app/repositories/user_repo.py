from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date

from ..models import User as UserModel
from ..models import CourseEnrollment as EnrollmentModel, Course as CourseModel, ModuleCompletion as ModuleCompletionModel, LessonCompletion as LessonCompletionModel

class UserUseCases:
    def __init__(self, db: Session):
        self.db = db

    def user_id_by_username(self, username: str):
        user_id = self.db.query(UserModel.id).filter(UserModel.username == username).scalar()
        if not user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não existe")
        return user_id

    def enroll(self, username: str, course_id: int):
        # 1. Buscar usuário completo
        user_id = self.user_id_by_username(username)
        
        # 2. Verificar se o curso existe
        course = self.db.query(CourseModel).filter(CourseModel.id == course_id).first()
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")
        
        # 3. Verificar se já está matriculado
        existing = self.db.query(EnrollmentModel).filter(
            EnrollmentModel.user_id == user_id,
            EnrollmentModel.course_id == course_id
        ).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Já matriculado neste curso")
        
        # 4. Criar matrícula
        enrollment = EnrollmentModel(
            user_id=user_id,
            course_id=course_id,
            registration_date=date.today()
        )
        
        # 5. Salvar no banco
        self.db.add(enrollment)
        self.db.commit()
        self.db.refresh(enrollment)

    def complete_module(self, username: str, module_id: int):
        # Lógica para marcar um módulo como completo para o usuário
        try:
            user_id = self.user_id_by_username(username)
            
            # Verificar se já foi completado
            existing_completion = self.db.query(ModuleCompletionModel).filter(
                ModuleCompletionModel.user_id == user_id,
                ModuleCompletionModel.module_id == module_id
            ).first()
            
            if existing_completion:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Módulo já foi completado anteriormente"
                )
            
            completion = ModuleCompletionModel(
                user_id=user_id,
                module_id=module_id,
                completion_date=date.today()
            )
            # Salvar no banco
            self.db.add(completion)
            self.db.commit()
            self.db.refresh(completion)

        except HTTPException:
            raise
        except Exception as e:  
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao completar módulo: " + str(e))
        
    def complete_lesson(self, username: str, lesson_id: int):
        # Lógica para marcar uma aula como completa para o usuário
        try:
            user_id = self.user_id_by_username(username)
            
            # Verificar se já foi completada
            existing_completion = self.db.query(LessonCompletionModel).filter(
                LessonCompletionModel.user_id == user_id,
                LessonCompletionModel.lesson_id == lesson_id
            ).first()
            
            if existing_completion:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Aula já foi completada anteriormente"
                )
            
            completion = LessonCompletionModel(
                user_id=user_id,
                lesson_id=lesson_id,
                completion_date=date.today()
            )
            # Salvar no banco
            self.db.add(completion)
            self.db.commit()
            self.db.refresh(completion)

        except HTTPException:
            raise
        except Exception as e:  
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao completar aula: " + str(e))


