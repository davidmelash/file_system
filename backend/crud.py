from sqlalchemy.orm import Session
import models
import schemas
import auth

def create_user(db: Session, user: schemas.UserCreate):
    """Create a new user"""
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username, 
        hashed_password=hashed_password,
        is_admin=False  # By default, users are not admins
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    """Get a user by username"""
    return db.query(models.User).filter(models.User.username == username).first()

def create_file(db: Session, file: schemas.FileCreate):
    """Create a new file record"""
    db_file = models.File(**file.dict())
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file

def get_file(db: Session, file_id: int):
    """Get a file by its ID"""
    return db.query(models.File).filter(models.File.id == file_id).first()


def delete_file(db: Session, file_id: int):
    """Delete a file record"""
    file = get_file(db, file_id)
    if file:
        db.delete(file)
        db.commit()

def get_all_files(db: Session):
    """Get all files with their download counts"""
    return db.query(models.File).all()


def get_all_users(db: Session):
    """Get all users"""
    return db.query(models.User).all()

def create_file_access(db: Session, file_access: schemas.FileAccessCreate):
    """Grant file access to a user"""
    db_file_access = models.FileAccess(**file_access.dict())
    db.add(db_file_access)
    db.commit()
    db.refresh(db_file_access)
    return db_file_access

def get_accessible_files(db: Session, user_id: int):
    """Get files accessible to a specific user"""
    return db.query(models.File).join(models.FileAccess).filter(models.FileAccess.user_id == user_id).all()

def get_file(db: Session, file_id: int):
    return db.query(models.File).filter(models.File.id == file_id).first()

def get_file_with_access(db: Session, file_id: int, user_id: int):
    """Get a file if the user has access"""
    return db.query(models.File).join(models.FileAccess).filter(
        models.File.id == file_id, 
        models.FileAccess.user_id == user_id
    ).first()

def increment_download_count(db: Session, file_id: int):
    """Increment the download count for a file"""

    file = get_file(db, file_id)
    if file:
        file.download_count += 1
        db.commit()