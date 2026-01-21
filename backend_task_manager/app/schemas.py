from pydantic import BaseModel, Field
from typing import Optional

class TaskListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: list["TaskOut"]
    
class LoginRequest(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=255)
    description: Optional[str] = Field(None, max_length=1000)


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskOut(TaskBase):
    id: int
    completed: bool

    class Config:
        orm_mode = True


class SignupRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=6, max_length=72)


TaskListResponse.model_rebuild()
