from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base user schema"""
    username: str

class UserCreate(UserBase):
    """Schema for user creation"""
    password: str

class User(UserBase):
    """User response schema"""
    id: int
    is_admin: bool

    class Config:
        orm_mode = True

class FileBase(BaseModel):
    """Base file schema"""
    filename: str
    filepath: str

class FileCreate(FileBase):
    """Schema for file creation"""
    pass

class File(FileBase):
    """File response schema"""
    id: int
    upload_date: datetime
    download_count: int

    class Config:
        orm_mode = True

class FileAccessCreate(BaseModel):
    """Schema for creating file access"""
    user_id: int
    file_id: int

class FileAccessResponse(BaseModel):
    """Response schema for file access"""
    user_id: int
    file_id: int
    id: int

    class Config:
        orm_mode = True