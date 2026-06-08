from pydantic import BaseModel

class Module(BaseModel):
    
    title: str
    course_id: int
    order_index: int | None = None

    class Config:
        orm_mode = True



