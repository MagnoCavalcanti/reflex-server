from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import status, HTTPException
from passlib.context import CryptContext
from jose import jwt, JWTError
from decouple import config
from datetime import datetime, timedelta, timezone

from ..schemas import UserLogin, User as UserSchema
from ..models import User as UserModel, RefreshToken as RefreshTokenModel


SECRET_KEY = config("SECRET_KEY")
ALGORITHM = config("ALGORITHM")
crypt_context = CryptContext(schemes=['sha256_crypt'])
ACCESS_TOKEN_MINUTES = 30
REFRESH_TOKEN_DAYS = 7

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

    def _generate_access_token(self, username: str):
        exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_MINUTES)
        payload = {
            "sub": username,
            "exp": exp
        }
        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return access_token

    def _generate_refresh_token(self, username: str):
        exp = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_DAYS)
        payload = {
            "sub": username,
            "exp": exp,
            "token_type": "refresh"
        }
        refresh_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return refresh_token, exp
        
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

        access_token = self._generate_access_token(user.username)
        refresh_token, refresh_exp = self._generate_refresh_token(user.username)

        refresh_token_db = RefreshTokenModel(
            user_id=user_db.id,
            token=refresh_token,
            expires_at=refresh_exp,
            revoked=False
        )
        self.db.add(refresh_token_db)
        self.db.commit()

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user_id": user_db.id,
            "username": user_db.username,
            "type_user": user_db.type_user
        }

    def refresh_access_token(self, refresh_token: str):
        try:
            data = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Refresh token inválido'
            )

        if data.get("token_type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Tipo de token inválido'
            )

        username = data.get("sub")
        user_on_db = self.db.query(UserModel).filter_by(username=username).first()
        if user_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Refresh token inválido'
            )

        token_on_db = self.db.query(RefreshTokenModel).filter_by(token=refresh_token, user_id=user_on_db.id).first()
        if token_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Refresh token inválido'
            )

        now = datetime.now(timezone.utc)
        expires_at = token_on_db.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if token_on_db.revoked or expires_at <= now:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Refresh token inválido'
            )

        new_access_token = self._generate_access_token(username)
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }

    def logout(self, refresh_token: str):
        token_on_db = self.db.query(RefreshTokenModel).filter_by(token=refresh_token).first()
        if token_on_db is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Refresh token inválido'
            )

        if token_on_db.revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Refresh token inválido'
            )

        token_on_db.revoked = True
        self.db.add(token_on_db)
        self.db.commit()
        return {"msg": "logout realizado com sucesso"}
    
    
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

