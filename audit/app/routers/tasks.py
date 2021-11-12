from datetime import datetime

from app.schemas import users
from app.utils import tasks as tasks_utils
from fastapi import APIRouter, Depends

from app.utils.dependencies import get_current_user

router = APIRouter()


@router.get("/balance")
async def get_balance(current_user: users.UserBase = Depends(get_current_user)):
    return await tasks_utils.get_balance(user_id=current_user.id)


@router.get("/statistic")
async def get_statistic(current_user: users.UserBase = Depends(get_current_user)):
    return await tasks_utils.get_statistic(datetime.now())


@router.get("/earned")
async def get_earned_today(current_user: users.UserBase = Depends(get_current_user)):
    return await tasks_utils.get_earned_money(datetime.now())


@router.get("/me/earned")
async def get_earned_today(current_user: users.UserBase = Depends(get_current_user)):
    return await tasks_utils.get_earned_money(datetime.now(), user_id=current_user.id)
