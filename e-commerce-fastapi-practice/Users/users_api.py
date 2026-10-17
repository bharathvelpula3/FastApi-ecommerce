import random
import string
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from pydantic.v1 import EmailStr
from sqlalchemy.orm import Session

from Users.user_database import get_user_db, UserBase, engine
from Users.users_models import User

user_router = APIRouter()
UserBase.metadata.create_all(bind=engine)

class UserResponse(BaseModel):
    id: int
    name: str
    email:str

class LoginRequest(BaseModel):
    username: str
    password: str

class RegistrationModel(BaseModel):
    name: str
    username: str
    password: str

@user_router.get('/users',status_code=200)
def get_users(user_db:Annotated[Session,Depends(get_user_db)]):
    users = user_db.query(User).all()

    if users is None:
        raise HTTPException(status_code=404, detail="User not found")
    return users

@user_router.post('/login',status_code=200)
def login(
    payload:LoginRequest,
    user_db: Annotated[Session, Depends(get_user_db)]):

    user = user_db.query(User).filter(User.email == payload.username).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.email == payload.username and user.hashPassword == payload.password:
        raise HTTPException(status_code=404, detail="Incorrect email or password")

    return {"authentication":True}

@user_router.post('/register',status_code=200,response_model=UserResponse)
def register(payload:RegistrationModel,
             user_db: Annotated[Session, Depends(get_user_db)]):
    new_user = user_db.query(User).filter(User.email == payload.username).first()
    if new_user is not None:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        id = random.randint(1, 100),
        name=payload.name,
        email= payload.username,
        hashPassword= payload.password
    )

    user_db.add(new_user)
    user_db.commit()
    user_db.refresh(new_user)

    return new_user
