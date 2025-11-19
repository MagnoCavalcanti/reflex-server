from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date

from ..models import User as UserModel
from ..models import CourseEnrollment as EnrollmentModel, Course as CourseModel, ModuleCompletion as ModuleCompletionModel, LessonCompletion as LessonCompletionModel, QuizAnswer as QuizAnswerModel, QuizOption as QuizOptionModel, QuizAttempt as QuizAttemptModel, QuizQuestion as QuizQuestionModel

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

    def answer_quiz(self, username: str, quiz_id: int, answer_option_ids: list[int]):
        try:
            user_id = self.user_id_by_username(username)

            questions = self.db.query(QuizQuestionModel).filter(
                QuizQuestionModel.quiz_id == quiz_id
            ).all()
            
            # Verificar se o usuário já respondeu ao quiz
            existing_attempt = self.db.query(QuizAttemptModel).filter(
                QuizAttemptModel.user_id == user_id,
                QuizAttemptModel.quiz_id == quiz_id
            ).first()
            
            if existing_attempt :
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Quiz já foi respondido anteriormente"
                )
            
            # Criar a resposta do quiz
            quiz_attempt = QuizAttemptModel(
                user_id=user_id,
                quiz_id=quiz_id,
                answer_date=date.today()
            )
            self.db.add(quiz_attempt)
            self.db.commit()
            self.db.refresh(quiz_attempt)
            
            # Adicionar as opções de resposta selecionadas
            score = 0
            for option_id in answer_option_ids:
                option = self.db.query(QuizOptionModel).filter(QuizOptionModel.id == option_id).first()
                if not option:
                    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Opção de resposta {option_id} não encontrada")
                if option.is_correct:
                    score += 1
                quiz_answer = QuizAnswerModel(
                    quiz_attempt_id=quiz_attempt.id,
                    question_id=option.question_id,
                    selected_option_id=option_id,
                    is_correct=option.is_correct
                )
                self.db.add(quiz_answer)
                self.db.commit()
                
            # Calcular a pontuação final

            
            score_percentage = (score / len(questions)) * 100 if questions else 0
            quiz_attempt.score = score_percentage

            self.db.add(quiz_attempt)
            self.db.commit()
            self.db.refresh(quiz_attempt)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao responder quiz: " + str(e))
