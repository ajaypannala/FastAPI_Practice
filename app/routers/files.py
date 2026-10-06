from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from pathlib import Path
import shutil

from app.models.user import User
from app.auth.dependencies import get_current_user

router = APIRouter(
    prefix="/files",
    tags=["Files"]
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
def upload_file(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    file_path = UPLOAD_DIR / file.filename

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename,
        "uploaded_by": current_user.email
    }