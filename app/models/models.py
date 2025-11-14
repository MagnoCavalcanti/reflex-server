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
        CheckConstraint("email ~ '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'", name='check_email_format'),
        CheckConstraint("telephone ~ '^\\(\\d{2}\\)\\s?\\d{5}-\\d{4}$'", name='check_telephone_format'),
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
    content_type = Column('content_type', String)
    done = Column('done', Boolean, default=False)
    module_id = Column('module_id', Integer, ForeignKey('modules.id'))
    
