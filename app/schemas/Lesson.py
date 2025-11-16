from pydantic import BaseModel

class Lesson(BaseModel):
    
    content_type: str
    done: bool = False
    module_id: int

    class Config:
        orm_mode = True


