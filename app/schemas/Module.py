from pydantic import BaseModel

class ModuleBase(BaseModel):
    title: str
    course_id: int

class ModuleCreate(ModuleBase):
    pass

class ModuleUpdate(ModuleBase):
    pass

class ModuleResponse(ModuleBase):
    id: int

    class Config:
        orm_mode = True
    


