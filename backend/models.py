from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class User(Base):
    """User model representing system users"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    

    file_accesses = relationship("FileAccess", back_populates="user")

class File(Base):
    """File model representing uploaded files"""
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    filepath = Column(String)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    download_count = Column(Integer, default=0)

    file_accesses = relationship("FileAccess", back_populates="file")

class FileAccess(Base):
    """Junction table to manage file access for users"""
    __tablename__ = "file_accesses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    file_id = Column(Integer, ForeignKey("files.id"))
    

    user = relationship("User", back_populates="file_accesses")
    file = relationship("File", back_populates="file_accesses")