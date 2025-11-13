from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from ..schemas import UserLogin, User as UserSchema
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