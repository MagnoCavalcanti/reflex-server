from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from ..schemas import User as UserSchema
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

