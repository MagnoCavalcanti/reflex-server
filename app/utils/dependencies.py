from ..core.db_connection import Session as sessionmaker
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import jwt
from fastapi.security import OAuth2PasswordBearer

from ..repositories.auth_repo import AuthUseCases

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://127.0.0.1:8000/auth/login")

def get_db_session():
    try:
        session = sessionmaker()
        yield session
    finally:
        session.close()  

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db_session)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifica o token
        uc = AuthUseCases(dbsession=db)
        payload = uc.verify_token(token)
        
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")
    except jwt.JWTError:
        raise credentials_exception