from pydantic import BaseModel, field_validator
from fastapi import status, HTTPException
import re

class User(BaseModel):

    username: str
    password: str
    email: str
    fullname: str
    telephone: str = '(XX)XXXXX-XXXX'

    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, v):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Email inválido. Use o formato usuario@dominio.com'
            )
        return v

    @field_validator('telephone')
    @classmethod
    def validate_telephone(cls, v):
        pattern = r'^\(\d{2}\)\s?\d{5}-\d{4}$'
        if not re.match(pattern, v):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Telefone deve estar no formato (XX) XXXXX-XXXX ou (XX)XXXXX-XXXX'
            )
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if len(v) < 8:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Senha deve ter no mínimo 8 caracteres'
            )
        
        if not re.search(r'[A-Z]', v):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Senha deve conter pelo menos uma letra maiúscula'
            )
        
        if not re.search(r'[a-z]', v):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Senha deve conter pelo menos uma letra minúscula'
            )
        
        if not re.search(r'\d', v):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Senha deve conter pelo menos um número'
            )
        
        return v

    class Config:
        orm_mode = True