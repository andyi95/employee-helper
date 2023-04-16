from users.models import User
from fastapi import APIRouter, HTTPException
from typing import List
from users.schemas import BaseUserOut, BaseUserCreate

router = APIRouter()

@router.get('/', response_model=List[BaseUserOut])
def get_users():
    users = User.all()
    return users

@router.post('/', response_model=BaseUserOut, status_code=201)
def create_user(*, user_in: BaseUserCreate):
    if User.get_by_email(email=user_in.email):
        raise HTTPException(
            status_code=400,
            detail='The user with email already exists'
        )