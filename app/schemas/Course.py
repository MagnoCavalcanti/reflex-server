from pydantic import BaseModel, field_validator
from fastapi import HTTPException, status

class Course(BaseModel):
    
    title: str
    description: str
    area: str | None = None
    level: str | None = None
    cover_image_url: str | None = None
    status: str = "rascunho"
    professor_id: int

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str):
        if value not in ("rascunho", "publicado"):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='status deve ser "rascunho" ou "publicado"'
            )
        return value

    class Config:
        orm_mode = True