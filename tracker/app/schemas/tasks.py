from datetime import datetime
from pydantic import BaseModel

from app.models.tasks import Status


class TaskBase(BaseModel):
    id: int
    title: str
    description: str
    status: Status
    created_at: datetime


class TaskCreate(BaseModel):
    title: str
    description: str
    assignee_id: int

    class Config:
        orm_mode = True


class TaskUpdateStatus(BaseModel):
    status: Status
