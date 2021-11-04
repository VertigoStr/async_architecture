from app.schemas import users
from app.utils import users as users_utils
from app.utils.dependencies import get_current_user
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.models.users import Role

router = APIRouter()


@router.get("/")
async def health_check():
    return {"Hello": "World"}


@router.post("/auth", response_model=users.TokenBase)
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_utils.get_user_by_email(email=form_data.username)

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not users_utils.validate_password(
        password=form_data.password, hashed_password=user["hashed_password"]
    ):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    return await users_utils.create_user_token(user_id=user["id"])


@router.post("/user", response_model=users.User)
async def create_user(user: users.UserCreate, current_user: users.User = Depends(get_current_user)):
    if current_user["role"] != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Permission denied")
    db_user = await users_utils.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await users_utils.create_user(user=user)


@router.patch("/user", response_model=users.User)
async def update_user(user: users.UserUpdate, current_user: users.User = Depends(get_current_user)):
    if current_user["role"] != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Permission denied")
    db_user = await users_utils.get_user(user.id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return await users_utils.update_user(user=user)


@router.get("/user/{user_id}")
async def get_user(user_id: int, current_user: users.User = Depends(get_current_user)):
    if current_user["role"] != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Permission denied")
    db_user = await users_utils.get_user(user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    return db_user


@router.delete("/user/{user_id}")
async def delete_user(user_id: int, current_user: users.User = Depends(get_current_user)):
    if current_user["role"] != Role.ADMIN:
        raise HTTPException(status_code=403, detail="Permission denied")
    db_user = await users_utils.get_user(user_id)
    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")
    await users_utils.delete_user(user_id)
    return {'status': 'ok'}


@router.get("/users/me", response_model=users.UserBase)
async def read_users_me(current_user: users.User = Depends(get_current_user)):
    return current_user
