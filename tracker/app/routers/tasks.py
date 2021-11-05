from app.schemas import tasks, users
from app.utils import tasks as tasks_utils
from fastapi import APIRouter, Depends

from app.utils.dependencies import get_current_user

router = APIRouter()


@router.post("/tasks", response_model=tasks.TaskBase)
async def create_task(task: tasks.TaskCreate, current_user: users.UserBase = Depends(get_current_user)):
    return await tasks_utils.create_task(creator_id=current_user['id'], task=task)


@router.patch("/tasks/{task_id}", response_model=tasks.TaskBase)
async def create_task(task_id: int, task: tasks.TaskUpdateStatus, current_user: users.UserBase = Depends(get_current_user)):
    await tasks_utils.update_task_status(task_id=task_id,
                                         actor_id=current_user['id'],
                                         to_status=task.status)
    return await tasks_utils.get_task(task_id)


@router.get("/tasks")
async def get_posts(page: int = 1):
    total_count = await tasks_utils.get_tasks_count()
    tasks = await tasks_utils.get_tasks(page)
    return {"total_count": total_count, "results": tasks}
