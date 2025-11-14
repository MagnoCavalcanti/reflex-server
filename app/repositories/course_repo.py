from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models import Course as CourseModel, User as UserModel
from ..schemas import Course as CourseSchema

class CoursesUseCases:
    def __init__(self, db_session: Session):
        self.db = db_session

    
    def list_courses(self):
        
        courses = self.db.query(CourseModel).all()
        return courses
    
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
            return new_course
        except Exception as e:
            self.db.rollback()
            raise HTTPException(detail="Erro ao criar o curso.", status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)