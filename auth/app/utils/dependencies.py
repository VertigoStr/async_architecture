from app.utils import users as users_utils
from app.producer import send_notice
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = await users_utils.get_user_by_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user


async def produce_user_updated(user_id: int):
    user = await users_utils.get_user(user_id)
    await send_notice({
        'action': 'user_updated',
        'data': {
            'id': user['id'],
            'is_active': user['is_active'],
            'role': user['role'],
            'email': user['email'],
        }
    })


async def produce_user_created(user_id: int):
    user = await users_utils.get_user(user_id)
    await send_notice({
        'action': 'user_created',
        'data': {
            'id': user['id'],
            'is_active': user['is_active'],
            'role': user['role'],
            'email': user['email'],
        }
    })


async def produce_user_inactive(user_id: int):
    await send_notice({
        'action': 'user_inactive',
        'data': {
            'id': user_id,
            'is_active': False,
        }
    })
