from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date

from ..models import User as UserModel
from ..models import CourseEnrollment as EnrollmentModel, Course as CourseModel
from ..schemas import User as UserSchema

class UserUseCases:
    def __init__(self, db: Session):
        self.db = db

    def enroll(self, username: str, course_id: int):
        # 1. Buscar usuário completo
        user = self.db.query(UserModel).filter(UserModel.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não existe")
        
        # 2. Verificar se o curso existe
        course = self.db.query(CourseModel).filter(CourseModel.id == course_id).first()
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")
        
        # 3. Verificar se já está matriculado
        existing = self.db.query(EnrollmentModel).filter(
            EnrollmentModel.user_id == user.id,
            EnrollmentModel.course_id == course_id
        ).first()
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Já matriculado neste curso")
        
        # 4. Criar matrícula
        enrollment = EnrollmentModel(
            user_id=user.id,
            course_id=course_id,
            registration_date=date.today()
        )
        
        # 5. Salvar no banco
        self.db.add(enrollment)
        self.db.commit()
        self.db.refresh(enrollment)
        

