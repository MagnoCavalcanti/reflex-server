from pydantic import BaseModel

class Course(BaseModel):
    
    title: str
    description: str
    professor_id: int

    class Config:
        orm_mode = True