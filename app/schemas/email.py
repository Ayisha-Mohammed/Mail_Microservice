from pydantic import BaseModel, EmailStr
from typing import Optional


class EmailCreate(BaseModel):
    to_email: EmailStr
    subject: str
    body: str


class EmailRead(BaseModel):
    id: int
    user_id: int
    to_email: EmailStr
    subject: str
    body: str
    status: str
    error_message: Optional[str]

    class Config:
        orm_mode = True
