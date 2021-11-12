import random
from datetime import datetime
from sqlalchemy import select

from sqlalchemy import func

from app.models.database import database
from app.models.tasks import task_price_table, task_balance_log_table, ActionType


async def log_balance_change(task_id: int, user_id: int, action_type: ActionType, price: float):
    query = task_balance_log_table.insert().values(
        task_id=task_id,
        user_id=user_id,
        action_type=action_type,
        price=price
    )
    await database.execute(query)


async def set_task_price(task_id: int):
    query = task_price_table.insert().values(
        task_id=task_id,
        price=random.randint(1, 1e2)
    )
    await database.execute(query)


async def set_task_completed(task_id: int, user_id: int):
    price = random.randint(20, 40)
    await log_balance_change(
        task_id=task_id,
        user_id=user_id,
        action_type=ActionType.ADD,
        price=price,
    )


async def set_task_assigned(task_id: int, user_id: int):
    price = random.randint(-20, -10)
    await log_balance_change(
        task_id=task_id,
        user_id=user_id,
        action_type=ActionType.DEBIT,
        price=price,
    )


async def get_balance(user_id: int):
    query = (
        select([func.sum(task_balance_log_table.c.price)])
        .select_from(task_balance_log_table)
        .where(task_balance_log_table.c.id == user_id)
    )
    return await database.fetch_val(query)


async def get_earned_money(date: datetime, user_id: int = None):
    query = (
        select([func.sum(task_balance_log_table.c.price)])
        .select_from(task_balance_log_table)
        .where(func.date(task_balance_log_table.c.created_at) == date.date())
    )
    if user_id is not None:
        query = query.where(task_balance_log_table.c.id == user_id)
    return await database.fetch_val(query)


async def get_statistic(date: datetime):
    return {'day': 10, 'month': 10, 'year': 20}
