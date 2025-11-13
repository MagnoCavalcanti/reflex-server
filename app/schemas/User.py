from pydantic import BaseModel

class User(BaseModel):

    username: str
    password: str
    email: str
    fullname: str
    telephone: str

    class Config:
        orm_mode = True