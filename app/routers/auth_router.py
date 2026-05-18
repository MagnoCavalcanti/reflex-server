from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas import UserLogin, User as UserSchema, RefreshTokenRequest, LogoutRequest
from ..utils import get_db_session
from ..repositories import AuthUseCases

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/register")
def register(user: UserSchema, db: Session = Depends(get_db_session)):
    auth_uc = AuthUseCases(db)
    auth_uc.register(user)

    return JSONResponse(
        content={ "msg": "sucess"},
        status_code= status.HTTP_201_CREATED
    )

@auth_router.post("/login")
def login(request_form_user: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db_session)
    ):
    auth_uc = AuthUseCases(db)
    user = UserLogin(
        username=request_form_user.username,
        password=request_form_user.password,
    )

    data_auth = auth_uc.login(user=user)

    return JSONResponse(
        content=data_auth,
        status_code=status.HTTP_200_OK
    )


@auth_router.post("/refresh")
def refresh_token(payload: RefreshTokenRequest, db: Session = Depends(get_db_session)):
    auth_uc = AuthUseCases(db)
    data_auth = auth_uc.refresh_access_token(payload.refresh_token)
    return JSONResponse(
        content=data_auth,
        status_code=status.HTTP_200_OK
    )


@auth_router.post("/logout")
def logout(payload: LogoutRequest, db: Session = Depends(get_db_session)):
    auth_uc = AuthUseCases(db)
    auth_uc.logout(payload.refresh_token)
    return JSONResponse(
        content={"msg": "success"},
        status_code=status.HTTP_200_OK
    )