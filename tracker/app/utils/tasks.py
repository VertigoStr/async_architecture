from sqlalchemy import func, desc

from app.schemas import tasks
from app.models.database import database
from app.models.tasks import task_table, task_status_log_table, Status


async def get_task(task_id: int):
    query = task_table.select().where(task_table.c.id == task_id)
    return await database.fetch_one(query)


async def log_status_change(task_id: int, actor_id: int, to_status: Status, from_status: Status = None):
    query = task_status_log_table.insert().values(
        task_id=task_id,
        actor_id=actor_id,
        to_status=to_status,
        from_status=from_status
    )
    await database.execute(query)


async def update_task_status(task_id: int, actor_id: int, to_status: Status):
    task = await get_task(task_id)
    query = task_table.update().where(
        task_table.c.id == task_id
    ).values(
        status=to_status
    )
    await database.execute(query)
    await log_status_change(
        task_id=task_id,
        actor_id=actor_id,
        to_status=to_status,
        from_status=task['status'],
    )


async def create_task(creator_id: int, task: tasks.TaskCreate):
    query = task_table.insert().values(
        creator_id=creator_id,
        status=Status.OPEN,
        **task.dict()
    )
    task_id = await database.execute(query)
    await log_status_change(
        task_id=task_id,
        actor_id=creator_id,
        to_status=Status.OPEN
    )
    return await get_task(task_id)


async def get_tasks(page: int, max_per_page: int = 10):
    offset1 = (page - 1) * max_per_page
    query = (
        task_table
        .select()
        .order_by(desc(task_table.c.created_at))
        .limit(max_per_page)
        .offset(offset1)
    )
    return await database.fetch_all(query)


async def get_tasks_count():
    query = task_table.count()
    return await database.fetch_val(query)
