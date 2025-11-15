from pydantic import BaseModel

class LessonBase(BaseModel):
    content_type: str
    done: bool = False
    module_id: int


class LessonCreate(LessonBase):
    pass


class LessonUpdate(LessonBase):
    pass


class LessonResponse(LessonBase):
    id: int

    class Config:
        orm_mode = True
        

