from datetime import datetime
from sqlalchemy import and_

from app.models.database import database
from app.models.users import users_table
from app.schemas import users


async def get_user(user_id: int):
    query = users_table.select().where(users_table.c.id == user_id)
    return await database.fetch_one(query)


async def get_user_by_token(token: str):
    query = users_table.select().where(
        and_(
            users_table.c.token == token,
            users_table.c.expires > datetime.now()
        )
    )
    return await database.fetch_one(query)


async def update_or_create_user(token: str, expires: str, user_data: users.UserBase):
    user = await get_user(user_data.id)
    # 2021-11-18T18:58:07.399284
    expires = datetime.strptime(expires, '%Y-%m-%dT%H:%M:%S.%f')
    if not user:
        query = users_table.insert().values(
            id=user_data.id,
            email=user_data.email,
            role=user_data.role,
            is_deleted=user_data.is_deleted,
            token=token,
            expires=expires
        )
        await database.execute(query)
    else:
        query = users_table.update().where(
            users_table.c.id == user['id']
        ).values(
            email=user_data.email,
            role=user_data.role,
            is_deleted=user_data.is_deleted,
            token=token,
            expires=expires
        )
        await database.execute(query)
