from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..models import Lesson as LessonModel, Module as ModuleModel, Course as CourseModel, User as UserModel, LessonVideo as LessonVideoModel, LessonQuiz as LessonQuizModel, QuizQuestion as QuizQuestionModel, QuizOption as QuizOptionModel
from ..schemas import Lesson as LessonSchema, LessonVideo as LessonVideoSchema, LessonQuiz as LessonQuizSchema, QuizQuestion as QuizQuestionSchema


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
            
            lesson = LessonModel(title=data.title, content_type=data.content_type, module_id=data.module_id)
            self.db.add(lesson)
            self.db.commit()
            self.db.refresh(lesson)
        except HTTPException:
            self.db.rollback()
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar aula: " + str(e))

        return lesson
    
    def get_by_id(self, lesson_id: int):
        lesson = self.db.query(LessonModel).filter(LessonModel.id == lesson_id).first()
        if not lesson:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aula não encontrada")
        return lesson
    
    def create_video(self, data: LessonVideoSchema, username: str):

        user_id = self.db.query(UserModel.id).filter(UserModel.username == username).scalar()

        # Verificar se a aula existe
        lesson = self.db.query(LessonModel).filter(LessonModel.id == data.lesson_id).first()
        if not lesson:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aula não encontrada")    
        module = self.db.query(ModuleModel).filter(ModuleModel.id == lesson.module_id).first()
        if not module:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Módulo não encontrado")
            
        # Verificar se o curso existe
        course = self.db.query(CourseModel).filter(CourseModel.id == module.course_id).first()
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")

        if course.professor_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, 
                    detail="Apenas o professor do curso pode criar aulas"
                )
        
        try:
            lesson_video = LessonVideoModel(lesson_id=data.lesson_id, video_url=data.video_url)
            self.db.add(lesson_video)
            self.db.commit()
            self.db.refresh(lesson_video)
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar vídeo da aula: " + str(e))
        return lesson_video
    
    def create_quiz(self, data: LessonQuizSchema, username: str):
        user_id = self.db.query(UserModel.id).filter(UserModel.username == username).scalar()

        # Verificar se a aula existe
        lesson = self.db.query(LessonModel).filter(LessonModel.id == data.lesson_id).first()
        if not lesson:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aula não encontrada")    
        module = self.db.query(ModuleModel).filter(ModuleModel.id == lesson.module_id).first()
        if not module:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Módulo não encontrado")
            
        # Verificar se o curso existe
        course = self.db.query(CourseModel).filter(CourseModel.id == module.course_id).first()
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")

        if course.professor_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, 
                    detail="Apenas o professor do curso pode criar aulas"
                )
        
        try:
            lesson_quiz = LessonQuizModel(lesson_id=data.lesson_id)
            self.db.add(lesson_quiz)
            self.db.commit()
            self.db.refresh(lesson_quiz)

            for question_data in data.questions:
                # Validar que tenha exatamente uma opção correta
                correct_options_count = sum(1 for option in question_data.options if option.is_correct)
                if correct_options_count != 1:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Cada pergunta deve ter exatamente uma opção correta. Pergunta '{question_data.question_text}' tem {correct_options_count}"
                    )
                
                quiz_question = QuizQuestionModel(
                    quiz_id=lesson_quiz.id,
                    question_text=question_data.question_text
                )
                self.db.add(quiz_question)
                self.db.commit()
                self.db.refresh(quiz_question)

                for option_data in question_data.options:
                    quiz_option = QuizOptionModel(
                        question_id=quiz_question.id,
                        option_text=option_data.option_text,
                        is_correct=option_data.is_correct
                    )
                    self.db.add(quiz_option)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao criar quiz da aula: " + str(e))
        return lesson_quiz

    def add_question_to_quiz(self, question: QuizQuestionSchema, username: str):
        user_id = self.db.query(UserModel.id).filter(UserModel.username == username).scalar()

        # Verificar se a aula existe
        quiz = self.db.query(LessonQuizModel).filter(LessonQuizModel.id == question.quiz_id).first()
        if not quiz:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Quiz não encontrado")
        lesson = self.db.query(LessonModel).filter(LessonModel.id == quiz.lesson_id).first()
        if not lesson:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aula não encontrada")    
        module = self.db.query(ModuleModel).filter(ModuleModel.id == lesson.module_id).first()
        if not module:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Módulo não encontrado")
            
        # Verificar se o curso existe
        course = self.db.query(CourseModel).filter(CourseModel.id == module.course_id).first()
        if not course:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado")

        if course.professor_id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, 
                    detail="Apenas o professor do curso pode alterar aulas"
                )
        
        try:
            # Validar que tenha exatamente uma opção correta
            correct_options_count = sum(1 for option in question.options if option.is_correct)
            if correct_options_count != 1:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"A pergunta deve ter exatamente uma opção correta. Recebido: {correct_options_count}"
                )
            
            quiz_question = QuizQuestionModel(
                quiz_id=question.quiz_id,
                question_text=question.question_text
            )
            self.db.add(quiz_question)
            self.db.commit()
            self.db.refresh(quiz_question)

            for option_data in question.options:
                quiz_option = QuizOptionModel(
                    question_id=quiz_question.id,
                    option_text=option_data.option_text,
                    is_correct=option_data.is_correct
                )
                self.db.add(quiz_option)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Erro ao adicionar pergunta ao quiz: " + str(e))
        return quiz_question

    def get_quiz_questions(self, quiz_id: int):
        questions = self.db.query(QuizQuestionModel).filter(QuizQuestionModel.quiz_id == quiz_id).all()
        if not questions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhuma pergunta encontrada para este quiz")
        result = []
        for question in questions:
            options = self.db.query(QuizOptionModel).filter(QuizOptionModel.question_id == question.id).all()
            result.append({
                "id": question.id,
                "question_text": question.question_text,
                "options": [{"id": option.id, "option_text": option.option_text} for option in options]
            })
        return result

    

