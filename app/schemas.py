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


# # Chat schema------------------


class ChatOut(BaseModel):
    id: UUID
    user1_id: UUID
    user2_id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# JWT Token schema------------------


class TokenData(BaseModel):
    id: Optional[UUID] = None


class Token(BaseModel):
    access_token: str
    token_type: str
