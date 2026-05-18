from pydantic import BaseModel

class Course(BaseModel):
    
    title: str
    description: str
    area: str | None = None
    level: str | None = None
    professor_id: int

    class Config:
        orm_mode = True