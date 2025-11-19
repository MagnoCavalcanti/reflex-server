from .base import Base
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, CheckConstraint, Boolean

from .enum import TipoUsuario
class User(Base):
    __tablename__ = 'users'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    username = Column('username', String, nullable=False, unique=True)
    password = Column('password', String, nullable=False)
    email = Column('email', String, nullable=False)
    fullname = Column('fullname', String)
    telephone = Column('telephone', String)
    type_user = Column('type_user', String, default=TipoUsuario.aluno, nullable=False)
    
    __table_args__ = (
        CheckConstraint(r"email ~ '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'", name='check_email_format'),
        CheckConstraint(r"telephone ~ '^\(\d{2}\)\s?\d{5}-\d{4}$'", name='check_telephone_format'),
        CheckConstraint("LENGTH(password) >= 8", name='check_password_length'),
        CheckConstraint("type_user IN ('A', 'P')", name='chk_type_user_values'),
    )

class Course(Base):
    __tablename__ = 'courses'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    title = Column('title', String, nullable=False, unique=True)
    description = Column('description', Text)
    professor_id = Column('professor_id', Integer, ForeignKey('users.id'))


class Module(Base):
    __tablename__ = 'modules'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    title = Column('title', String, nullable=False)
    course_id = Column('course_id', Integer, ForeignKey('courses.id'))

class CourseEnrollment(Base):
    __tablename__ = 'course_enrollments'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    registration_date = Column('registration_date', Date)
    user_id = Column('user_id', Integer, ForeignKey('users.id'))
    course_id = Column('course_id', Integer, ForeignKey('courses.id'))

class Lesson(Base):
    __tablename__ = 'lessons'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    title = Column('title', String, nullable=False)
    content_type = Column('content_type', String)
    module_id = Column('module_id', Integer, ForeignKey('modules.id'))

    __table_args__ = (
        CheckConstraint("content_type IN ('V', 'Q')", name='chk_content_type_values'),
    )
    
class LessonVideo(Base):
    __tablename__ = 'lesson_videos'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    lesson_id = Column('lesson_id', Integer, ForeignKey('lessons.id'))
    video_url = Column('video_url', String, nullable=False)

class LessonQuiz(Base):
    __tablename__ = 'lesson_quizzes'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    lesson_id = Column('lesson_id', Integer, ForeignKey('lessons.id'))

class QuizQuestion(Base):
    __tablename__ = 'quiz_questions'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    quiz_id = Column('quiz_id', Integer, ForeignKey('lesson_quizzes.id'))
    question_text = Column('question_text', Text, nullable=False)

class QuizOption(Base):
    __tablename__ = 'quiz_options'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    question_id = Column('question_id', Integer, ForeignKey('quiz_questions.id'))
    option_text = Column('option_text', Text, nullable=False)
    is_correct = Column('is_correct', Boolean, default=False)

class ModuleCompletion(Base):
    __tablename__ = 'module_completions'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('users.id'))
    module_id = Column('module_id', Integer, ForeignKey('modules.id'))
    completion_date = Column('completion_date', Date)

class LessonCompletion(Base):
    __tablename__ = 'lesson_completions'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('users.id'))
    lesson_id = Column('lesson_id', Integer, ForeignKey('lessons.id'))
    completion_date = Column('completion_date', Date)

class QuizAttempt(Base):
    __tablename__ = 'quiz_attempts'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    user_id = Column('user_id', Integer, ForeignKey('users.id'))
    quiz_id = Column('quiz_id', Integer, ForeignKey('lesson_quizzes.id'))
    attempt_date = Column('attempt_date', Date)
    score = Column('score', Integer)

class QuizAnswer(Base):
    __tablename__ = 'quiz_answers'
    id = Column('id', Integer, autoincrement=True, primary_key=True)
    attempt_id = Column('attempt_id', Integer, ForeignKey('quiz_attempts.id'))
    question_id = Column('question_id', Integer, ForeignKey('quiz_questions.id'))
    selected_option_id = Column('selected_option_id', Integer, ForeignKey('quiz_options.id'))
    is_correct = Column('is_correct', Boolean, default=False)

