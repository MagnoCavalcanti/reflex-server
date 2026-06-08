from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy import or_

from ..models import Course as CourseModel, User as UserModel, Module as ModuleModel, Lesson as LessonModel, CourseEnrollment as CourseEnrollmentModel, LessonQuiz as LessonQuizModel, QuizQuestion as QuizQuestionModel, QuizAnswer as QuizAnswerModel
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
            "cover_image_url": course.cover_image_url,
            "status": course.status,
            "professor_id": course.professor_id,
            "professor_name": (
                professor.fullname.strip()
                if professor and professor.fullname and professor.fullname.strip()
                else (professor.username if professor else None)
            ),
            "created_at": course.created_at.isoformat() if course.created_at else None,
            "updated_at": course.updated_at.isoformat() if course.updated_at else None,
        }

        if not include_modules:
            return payload

        modules = (
            self.db.query(ModuleModel)
            .filter(ModuleModel.course_id == course.id)
            .order_by(ModuleModel.order_index.asc(), ModuleModel.id.asc())
            .all()
        )
        modules_payload = []
        for module in modules:
            lessons = self.db.query(LessonModel).filter(LessonModel.module_id == module.id).all()
            modules_payload.append(
                {
                    "id": module.id,
                    "title": module.title,
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

        query = query.order_by(CourseModel.created_at.desc())

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

    def update_course(self, course_id: int, course_data: CourseSchema):
        course = self.db.query(CourseModel).filter(CourseModel.id == course_id).first()
        if not course:
            raise HTTPException(
                detail="Curso não encontrado",
                status_code=status.HTTP_404_NOT_FOUND
            )

        professor = self.db.query(UserModel).filter(
            UserModel.id == course_data.professor_id,
            UserModel.type_user == "P"
        ).first()
        if not professor:
            raise HTTPException(
                detail="Professor não encontrado ou inválido.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        course.title = course_data.title
        course.description = course_data.description
        course.area = course_data.area
        course.level = course_data.level
        course.cover_image_url = course_data.cover_image_url
        course.status = course_data.status
        course.professor_id = course_data.professor_id

        try:
            self.db.add(course)
            self.db.commit()
            self.db.refresh(course)
            return self._serialize_course(course, professor=professor, include_modules=False)
        except Exception:
            self.db.rollback()
            raise HTTPException(
                detail="Erro ao atualizar o curso.",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def get_professor_course_enrollment_metrics(self, professor_id: int):
        professor = self.db.query(UserModel).filter(
            UserModel.id == professor_id,
            UserModel.type_user == "P"
        ).first()
        if not professor:
            raise HTTPException(
                detail="Professor não encontrado ou inválido.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        courses = self.db.query(CourseModel).filter(CourseModel.professor_id == professor_id).all()
        if not courses:
            return {
                "professor_id": professor_id,
                "courses_total": 0,
                "total_enrollments": 0,
                "courses_by_enrollments": []
            }

        course_ids = [course.id for course in courses]
        enrollments = self.db.query(CourseEnrollmentModel).filter(
            CourseEnrollmentModel.course_id.in_(course_ids)
        ).all()

        enrollments_by_course: dict[int, int] = {course_id: 0 for course_id in course_ids}
        for enrollment in enrollments:
            enrollments_by_course[enrollment.course_id] = enrollments_by_course.get(enrollment.course_id, 0) + 1

        courses_by_enrollments = sorted(
            [
                {
                    "course_id": course.id,
                    "title": course.title,
                    "enrollments": enrollments_by_course.get(course.id, 0)
                }
                for course in courses
            ],
            key=lambda item: (-item["enrollments"], item["title"].lower())
        )

        return {
            "professor_id": professor_id,
            "courses_total": len(courses),
            "total_enrollments": len(enrollments),
            "courses_by_enrollments": courses_by_enrollments
        }

    def get_course_quiz_question_metrics(self, course_id: int, professor_id: int):
        course = self.db.query(CourseModel).filter(CourseModel.id == course_id).first()
        if not course:
            raise HTTPException(
                detail="Curso não encontrado",
                status_code=status.HTTP_404_NOT_FOUND
            )

        if course.professor_id != professor_id:
            raise HTTPException(
                detail="Apenas o professor dono do curso pode visualizar métricas de exercícios",
                status_code=status.HTTP_403_FORBIDDEN
            )

        modules = self.db.query(ModuleModel).filter(ModuleModel.course_id == course_id).all()
        if not modules:
            return {
                "course_id": course_id,
                "questions_total": 0,
                "answers_total": 0,
                "correct_answers_total": 0,
                "questions": []
            }

        module_by_id = {module.id: module for module in modules}
        module_ids = list(module_by_id.keys())

        lessons = self.db.query(LessonModel).filter(LessonModel.module_id.in_(module_ids)).all()
        if not lessons:
            return {
                "course_id": course_id,
                "questions_total": 0,
                "answers_total": 0,
                "correct_answers_total": 0,
                "questions": []
            }

        lesson_by_id = {lesson.id: lesson for lesson in lessons}
        lesson_ids = list(lesson_by_id.keys())

        quizzes = self.db.query(LessonQuizModel).filter(LessonQuizModel.lesson_id.in_(lesson_ids)).all()
        if not quizzes:
            return {
                "course_id": course_id,
                "questions_total": 0,
                "answers_total": 0,
                "correct_answers_total": 0,
                "questions": []
            }

        quiz_by_id = {quiz.id: quiz for quiz in quizzes}
        quiz_ids = list(quiz_by_id.keys())

        questions = self.db.query(QuizQuestionModel).filter(QuizQuestionModel.quiz_id.in_(quiz_ids)).all()
        if not questions:
            return {
                "course_id": course_id,
                "questions_total": 0,
                "answers_total": 0,
                "correct_answers_total": 0,
                "questions": []
            }

        question_ids = [question.id for question in questions]
        answers = self.db.query(QuizAnswerModel).filter(QuizAnswerModel.question_id.in_(question_ids)).all()

        answers_by_question: dict[int, dict[str, int]] = {}
        for answer in answers:
            stats = answers_by_question.setdefault(answer.question_id, {"total": 0, "correct": 0})
            stats["total"] += 1
            if answer.is_correct:
                stats["correct"] += 1

        questions_payload = []
        total_answers = 0
        total_correct_answers = 0

        for question in questions:
            stats = answers_by_question.get(question.id, {"total": 0, "correct": 0})
            total = stats["total"]
            correct = stats["correct"]
            total_answers += total
            total_correct_answers += correct
            accuracy = round((correct / total) * 100, 2) if total > 0 else 0.0

            quiz = quiz_by_id.get(question.quiz_id)
            lesson = lesson_by_id.get(quiz.lesson_id) if quiz else None
            module = module_by_id.get(lesson.module_id) if lesson else None

            questions_payload.append(
                {
                    "question_id": question.id,
                    "question_text": question.question_text,
                    "module_id": module.id if module else None,
                    "module_title": module.title if module else None,
                    "lesson_id": lesson.id if lesson else None,
                    "lesson_title": lesson.title if lesson else None,
                    "total_answers": total,
                    "correct_answers": correct,
                    "accuracy_percent": accuracy,
                    "order_index": module.order_index if module else 9999,
                }
            )

        questions_payload = sorted(
            questions_payload,
            key=lambda item: (
                item["order_index"],
                item["lesson_id"] or 0,
                item["question_id"]
            )
        )
        for item in questions_payload:
            del item["order_index"]

        return {
            "course_id": course_id,
            "questions_total": len(questions_payload),
            "answers_total": total_answers,
            "correct_answers_total": total_correct_answers,
            "questions": questions_payload
        }