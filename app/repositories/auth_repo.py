from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import status, HTTPException
from passlib.context import CryptContext
from jose import jwt, JWTError
from decouple import config
from datetime import datetime, timedelta, timezone

from ..schemas import UserLogin, User as UserSchema
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
        
    def login(self, user: UserLogin):
        user_db = self.db.query(UserModel).filter_by(username=user.username).first()

        if user_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Login inválido!'
            )
        
        if not crypt_context.verify(user.password, user_db.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Login inválido!'
            )
        
        exp = datetime.now(timezone.utc) + timedelta(minutes=30)
        
        payload = {
            "sub": user.username,
            "exp": exp
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            "access_token": access_token,  # Mudança para "access_token"
            "token_type": "bearer",          # Adicionando "token_type"
            "exp": exp.isoformat("T")        # Adicionando "exp"
        }
        
    
    def verify_token(self, token: str):
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_on_db = self.db.query(UserModel).filter_by(username=data['sub']).first()

            if user_on_db is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Token inválido'
                )
            return data
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token inválido'
            )

