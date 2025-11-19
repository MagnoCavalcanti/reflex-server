from pydantic import BaseModel
from datetime import date

class QuizAnswer(BaseModel):
    attempt_id: int
    question_id: int
    selected_option_id: int

    class Config:
        orm_mode = True

class QuizAttempt(BaseModel):
    user_id: int
    quiz_id: int
    attempt_date: date = date.today()
    score: int

    class Config:
        orm_mode = True

