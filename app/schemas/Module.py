from pydantic import BaseModel

class Module(BaseModel):
    
    title: str
    course_id: int

    class Config:
        orm_mode = True



