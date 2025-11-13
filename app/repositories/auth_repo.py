from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import status, HTTPException
from passlib.context import CryptContext
from jose import jwt, JWTError
from decouple import config

from ..schemas import User as UserSchema
from ..models import User as UserModel


SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
crypt_context = CryptContext(schemes=['sha256_crypt'])

class AuthUseCases:
    
    def __init__(self, db_session: Session):
        self.db = db_session

    def register(self, user: UserSchema):
        try:
            user_data = user.__dict__.copy()
            user_data['password'] = crypt_context.hash(user_data['password'])
            user_db = UserModel(**user_data)

        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="dados inválido"
            )
        
        try: 
            self.db.add(user_db)
            self.db.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao salvar dados"
            )

