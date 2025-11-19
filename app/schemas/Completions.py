from pydantic import BaseModel
from datetime import date

class ModuleCompletion(BaseModel):
    user_id: int
    module_id: int
    completion_date: date = date.today()

    class Config:
        orm_mode = True

class LessonCompletion(BaseModel):
    user_id: int
    lesson_id: int
    completion_date: date = date.today()

    class Config:
        orm_mode = True
