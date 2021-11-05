from pydantic import BaseModel, EmailStr

from app.models.users import Role


class UserBase(BaseModel):
    id: int
    email: EmailStr
    role: Role
    is_deleted: bool
