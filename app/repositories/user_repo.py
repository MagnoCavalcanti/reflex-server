from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date

from ..models import User as UserModel
from ..models import CourseEnrollment as EnrollmentModel, Course as CourseModel, Module as ModuleModel, Lesson as LessonModel, ModuleCompletion as ModuleCompletionModel, LessonCompletion as LessonCompletionModel, QuizAnswer as QuizAnswerModel, QuizOption as QuizOptionModel, QuizAttempt as QuizAttemptModel, QuizQuestion as QuizQuestionModel

class UserUseCases:
    def __init__(self, db: Session):
        self.db = db

    def user_id_by_username(self, username: str):
        user_id = self.db.query(UserModel.id).filter(UserModel.username == username).scalar()
        if not user_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não existe")
        return user_id

    def ensure_professor(self, username: str):
        user = self.db.query(UserModel).filter(UserModel.username == username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não existe")
        if user.type_user != "P":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acesso permitido apenas para professores"
            )
        return user

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

    def list_students_by_course(self, course_id: int, professor_username: str):
        professor_id = self.user_id_by_username(professor_username)
        course = self.db.query(CourseModel).filter(CourseModel.id == course_id).first()
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")

        if course.professor_id != professor_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Apenas o professor dono do curso pode listar alunos"
            )

        enrollments = self.db.query(EnrollmentModel).filter(EnrollmentModel.course_id == course_id).all()
        if not enrollments:
            return []

        student_ids = [enrollment.user_id for enrollment in enrollments]
        students = self.db.query(UserModel).filter(UserModel.id.in_(student_ids)).all()
        student_by_id = {student.id: student for student in students}

        return [
            {
                "id": enrollment.id,
                "registration_date": enrollment.registration_date.isoformat() if enrollment.registration_date else None,
                "student": {
                    "id": enrollment.user_id,
                    "username": student_by_id[enrollment.user_id].username if enrollment.user_id in student_by_id else None,
                    "fullname": student_by_id[enrollment.user_id].fullname if enrollment.user_id in student_by_id else None,
                    "email": student_by_id[enrollment.user_id].email if enrollment.user_id in student_by_id else None,
                    "telephone": student_by_id[enrollment.user_id].telephone if enrollment.user_id in student_by_id else None
                }
            }
            for enrollment in enrollments
        ]

    def get_student_course_progress(self, username: str):
        user_id = self.user_id_by_username(username)
        enrollments = self.db.query(EnrollmentModel).filter(EnrollmentModel.user_id == user_id).all()
        if not enrollments:
            return []

        course_ids = [enrollment.course_id for enrollment in enrollments]
        courses = self.db.query(CourseModel).filter(CourseModel.id.in_(course_ids)).all()
        course_by_id = {course.id: course for course in courses}

        modules = self.db.query(ModuleModel).filter(ModuleModel.course_id.in_(course_ids)).all()
        module_ids = [module.id for module in modules]
        course_id_by_module_id = {module.id: module.course_id for module in modules}

        lessons = self.db.query(LessonModel).filter(LessonModel.module_id.in_(module_ids)).all() if module_ids else []
        lessons_by_course_id: dict[int, list[int]] = {}
        for lesson in lessons:
            course_id = course_id_by_module_id.get(lesson.module_id)
            if course_id is None:
                continue
            lessons_by_course_id.setdefault(course_id, []).append(lesson.id)

        all_lesson_ids = [lesson.id for lesson in lessons]
        completed_lessons = (
            self.db.query(LessonCompletionModel)
            .filter(
                LessonCompletionModel.user_id == user_id,
                LessonCompletionModel.lesson_id.in_(all_lesson_ids),
            )
            .all()
            if all_lesson_ids
            else []
        )
        completed_lesson_ids = {item.lesson_id for item in completed_lessons}

        payload = []
        for enrollment in enrollments:
            lesson_ids = lessons_by_course_id.get(enrollment.course_id, [])
            total_lessons = len(lesson_ids)
            completed_count = sum(1 for lesson_id in lesson_ids if lesson_id in completed_lesson_ids)
            progress_percent = round((completed_count / total_lessons) * 100, 2) if total_lessons > 0 else 0.0

            course = course_by_id.get(enrollment.course_id)
            payload.append(
                {
                    "course_id": enrollment.course_id,
                    "course_title": course.title if course else None,
                    "total_lessons": total_lessons,
                    "completed_lessons": completed_count,
                    "progress_percent": progress_percent,
                    "is_completed": total_lessons > 0 and completed_count == total_lessons,
                }
            )

        return payload

    def get_completed_lesson_ids_by_course(self, username: str, course_id: int):
        user_id = self.user_id_by_username(username)

        course = self.db.query(CourseModel).filter(CourseModel.id == course_id).first()
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")

        modules = self.db.query(ModuleModel.id).filter(ModuleModel.course_id == course_id).all()
        module_ids = [module_id for (module_id,) in modules]
        if not module_ids:
            return []

        lessons = self.db.query(LessonModel.id).filter(LessonModel.module_id.in_(module_ids)).all()
        lesson_ids = [lesson_id for (lesson_id,) in lessons]
        if not lesson_ids:
            return []

        completions = (
            self.db.query(LessonCompletionModel.lesson_id)
            .filter(
                LessonCompletionModel.user_id == user_id,
                LessonCompletionModel.lesson_id.in_(lesson_ids),
            )
            .all()
        )
        return [lesson_id for (lesson_id,) in completions]

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
            if not questions:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Quiz não encontrado ou sem perguntas cadastradas"
                )
            
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

            options = self.db.query(QuizOptionModel).filter(
                QuizOptionModel.question_id.in_([question.id for question in questions])
            ).all()
            option_by_id = {option.id: option for option in options}
            question_ids = {question.id for question in questions}
            answered_by_question_id: dict[int, int] = {}
            for option_id in answer_option_ids:
                option = option_by_id.get(option_id)
                if not option:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Opção de resposta {option_id} não encontrada"
                    )
                if option.question_id not in question_ids:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Opção de resposta não pertence a este quiz"
                    )
                if option.question_id in answered_by_question_id:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Mais de uma resposta para a mesma pergunta"
                    )
                answered_by_question_id[option.question_id] = option_id

            missing_question_ids = [question.id for question in questions if question.id not in answered_by_question_id]
            if missing_question_ids:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="É necessário responder todas as perguntas do quiz"
                )
            
            # Criar a resposta do quiz
            quiz_attempt = QuizAttemptModel(
                user_id=user_id,
                quiz_id=quiz_id,
                attempt_date=date.today(),
                score=0
            )
            self.db.add(quiz_attempt)
            self.db.commit()
            self.db.refresh(quiz_attempt)
            
            # Adicionar as opções de resposta selecionadas
            score = 0
            for question in questions:
                option_id = answered_by_question_id[question.id]
                option = option_by_id[option_id]
                if option.is_correct:
                    score += 1
                quiz_answer = QuizAnswerModel(
                    attempt_id=quiz_attempt.id,
                    question_id=option.question_id,
                    selected_option_id=option_id,
                    is_correct=option.is_correct
                )
                self.db.add(quiz_answer)
                
            # Calcular a pontuação final
            score_percentage = int(round((score / len(questions)) * 100)) if questions else 0
            quiz_attempt.score = score_percentage

            self.db.add(quiz_attempt)
            self.db.commit()
            self.db.refresh(quiz_attempt)
            return {
                "attempt_id": quiz_attempt.id,
                "score": quiz_attempt.score,
                "correct_answers": score,
                "total_questions": len(questions),
            }

        except HTTPException:
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao responder quiz: " + str(e))
