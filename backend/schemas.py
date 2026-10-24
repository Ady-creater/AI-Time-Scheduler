# Pydantic data validation

from pydantic import BaseModel, ConfigDict, Field, EmailStr
from agent_logic import User, UserProfile, Task
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    username: str = Field(min_length=1, max_length=50)
    email: EmailStr = Field(max_length=120)
    profile: UserProfile
    schedule: list[Task]

class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    image_file: str | None
    image_path: str

class UserPrivate(UserPublic):
    email: EmailStr

class UserUpdate(BaseModel):
    username: str = Field(default="", min_length=1, max_length=50)
    email: EmailStr = Field(default="", max_length=120) 
    image_file: str | None = Field(default=None, min_length=1, max_length=200)

class Token(BaseModel):
    access_token: str
    token_type: str

class ScheduleBase(BaseModel):
    schedule: list[dict]