from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, validator, Field

from app.models.users import Role


class TokenBase(BaseModel):
    """ Return response data """
    token: UUID4 = Field(..., alias="access_token")
    expires: datetime
    token_type: Optional[str] = "bearer"

    class Config:
        allow_population_by_field_name = True

    @validator("token")
    def hexlify_token(cls, value):
        return value.hex


class UserBase(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    role: Role


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Role


class UserUpdate(BaseModel):
    id: int
    is_active: bool
    role: Role


class User(UserBase):
    role: Role
    token: TokenBase = {}
