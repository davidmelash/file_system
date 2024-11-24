from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import uvicorn
import os

from database import SessionLocal, engine
import models
import schemas
import crud
import auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="File Sharing Platform")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://0.0.0.0:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/register", response_model=schemas.User)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new regular user"""
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db, user)

@app.post("/token")
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    """Generate access token for authentication"""
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer", "username": user.username, "is_admin": user.is_admin}


@app.post("/admin/upload", response_model=schemas.File)
def upload_file(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """Admin route to upload a file"""

    os.makedirs("uploads", exist_ok=True)
    

    file_location = os.path.join("uploads", file.filename)
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    

    file_create = schemas.FileCreate(
        filename=file.filename, 
        filepath=file_location
    )
    return crud.create_file(db, file_create)


@app.get("/admin/users")
def upload_file(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """Admin route to get all users"""
    return crud.get_all_users(db)


@app.delete("/admin/files/{file_id}")
def delete_file(
    file_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """Admin route to delete a file"""
    file = crud.get_file(db, file_id)
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    

    if os.path.exists(file.filepath):
        os.remove(file.filepath)
    

    crud.delete_file(db, file_id)
    return {"detail": "File deleted successfully"}

@app.get("/admin/files")
def list_files(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """Admin route to list all files with download counts"""
    return crud.get_all_files(db)


@app.get("/user/files")
def list_accessible_files(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """List files accessible to the current user"""
    return crud.get_accessible_files(db, current_user.id)

@app.get("/user/download/{file_id}")
def download_file(
    file_id: int, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    """Download a file if user has access"""

    if current_user.is_admin:
        file = crud.get_file(db, file_id)
        if not file:
            raise HTTPException(status_code=404, detail="Not found")
    else:
        file = crud.get_file_with_access(db, file_id, current_user.id)
        if not file:
            raise HTTPException(status_code=403, detail="Access denied")
        

    crud.increment_download_count(db, file_id)
    
    return FileResponse(
        path=file.filepath, 
        filename=file.filename
    )


@app.post("/admin/grant-access")
def grant_file_access(
    file_access: schemas.FileAccessCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    """Grant access to a file for specific users"""
    return crud.create_file_access(db, file_access)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)