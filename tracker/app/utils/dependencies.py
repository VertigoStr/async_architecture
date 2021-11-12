from app.producer import send_notice
from app.utils import users as users_utils
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
    if user["is_deleted"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user


async def produce_task_created(task_id: int):
    await send_notice({
        'action': 'task_created',
        'data': {
            'task_id': task_id,
        }
    })


async def produce_task_assigned(user_id: int, task_id: int):
    await send_notice({
        'action': 'task_assigned',
        'data': {
            'task_id': task_id,
            'user_id': user_id,
        }
    })


async def produce_task_completed(user_id: int, task_id: int):
    await send_notice({
        'action': 'task_completed',
        'data': {
            'task_id': task_id,
            'user_id': user_id,
        }
    })
