import aiohttp
from os import environ

from app.schemas import users
from app.utils import users as users_utils
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

OAUTH_HOST = environ.get("OAUTH_HOST", "http://127.0.0.1:8001")
router = APIRouter()


@router.post("/auth")
async def auth(form_data: OAuth2PasswordRequestForm = Depends()):
    async with aiohttp.ClientSession() as session:
        data = {
            'username': form_data.username,
            'password': form_data.password
        }
        async with session.post(f'{OAUTH_HOST}/auth', data=data) as resp:
            result = await resp.json()
        token = result['access_token']
        expire_time = result['expires']
        headers = {'Authorization': f'Bearer {token}'}
        async with session.get(f'{OAUTH_HOST}/users/me', headers=headers) as resp:
            result = await resp.json()
            user = users.UserBase(
                id=result['id'],
                email=result['email'],
                role=result['role'],
                is_deleted=not result['is_active'],
            )
        await users_utils.update_or_create_user(token, expire_time, user)
    return {'access_token': token, 'token_type': 'bearer', 'expires': expire_time}
