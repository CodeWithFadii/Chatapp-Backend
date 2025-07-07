from datetime import datetime
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr


# User schema ------------------


class UserBase(BaseModel):
    user_name: str
    password: str


class UserRegister(UserBase):
    pass


class UserLogin(UserBase):
    pass


class User(BaseModel):
    id: UUID
    user_name: str
    name: Optional[str] = None
    profile_img: Optional[str] = None
    created_at: datetime

    model_config = {"from_attributes": True, "json_encoders": {UUID: lambda v: str(v)}}


class UserEdit(BaseModel):
    name: str
    profile_img: Optional[str] = None


class UserOut(BaseModel):
    user: User


class UserAuthOut(BaseModel):
    access_token: str
    token_type: str
    user: User


class ChangePassword(BaseModel):
    user_name: str
    old_password: str
    new_password: str


class ChangePasswordOut(BaseModel):
    success: bool
    message: str


class ChangeName(BaseModel):
    name: str


class EmailRequest(BaseModel):
    email: EmailStr


class CodeRequest(BaseModel):
    code: str


# # Task schema------------------


# class TaskBase(BaseModel):
#     title: str
#     details: str
#     team_members: Optional[List[str]] = []
#     date: str
#     time: str


# class TaskCreate(TaskBase):
#     owner_id: Optional[str] = ""
#     pass


# class TaskUpdate(TaskBase):
#     pass


# class Task(BaseModel):
#     id: UUID
#     owner_id: str
#     title: str
#     details: str
#     team_members: Optional[List[str]] = []
#     date: str
#     time: str
#     is_completed: Optional[bool] = False
#     created_at: datetime

#     model_config = {"from_attributes": True, "json_encoders": {UUID: lambda v: str(v)}}


# JWT Token schema------------------


class TokenData(BaseModel):
    id: Optional[UUID] = None


class Token(BaseModel):
    access_token: str
    token_type: str


# Pagination schema------------------


class PaginatedUsers(BaseModel):
    users: List[User]
    total_count: int
    next_cursor: Optional[UUID]


# Otp schema------------------


# class OtpOut(BaseModel):
#     otp: str
#     message: str


# class Otp(BaseModel):
#     email: EmailStr
