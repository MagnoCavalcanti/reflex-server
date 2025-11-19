from pydantic import BaseModel, field_validator, model_validator
from typing import Optional
from fastapi import HTTPException, status


class LessonVideo(BaseModel):
    lesson_id: int
    video_url: str

    class Config:
        orm_mode = True


class QuizOption(BaseModel):
    question_id: int
    option_text: str
    is_correct: bool = False

    class Config:
        orm_mode = True

class QuizQuestion(BaseModel):
    quiz_id: int
    question_text: str
    options: list[QuizOption]

    class Config:
        orm_mode = True

class LessonQuiz(BaseModel):
    lesson_id: int
    questions: list[QuizQuestion]

    class Config:
        orm_mode = True

class Lesson(BaseModel):
    
    title: str
    content_type: str
    module_id: int

    @field_validator('content_type')
    @classmethod
    def validate_content_type(cls, v):
        if v not in ('V', 'Q'):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='content_type deve ser "V" (video) ou "Q" (quiz)'
            )
        return v


    class Config:
        orm_mode = True

