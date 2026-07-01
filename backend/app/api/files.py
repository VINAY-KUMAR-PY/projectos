from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.config.settings import settings
from app.database.connection import get_db
from app.models.user import User
from app.models.workspace import ProjectFile
from app.services.workspace_service import get_file, get_project
from app.utils.file_processing import extract_text_from_file, extract_video_transcript

router = APIRouter(prefix="/api/files", tags=["Files"])


def save_upload(project_id: int, upload: UploadFile) -> tuple[str, int]:
    upload_dir = Path(settings.upload_dir) / str(project_id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    safe_name = Path(upload.filename or "upload.bin").name
    target = upload_dir / safe_name
    content = upload.file.read()
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(status_code=413, detail="File exceeds upload limit")
    target.write_bytes(content)
    return str(target), len(content)


@router.post("/upload/{project_id}", status_code=status.HTTP_201_CREATED)
def upload_file(project_id: int, upload: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    get_project(db, project_id, current_user.id)
    path, size = save_upload(project_id, upload)
    content_type = upload.content_type or "application/octet-stream"
    extracted = extract_video_transcript(path) if content_type.startswith("video/") else extract_text_from_file(path, content_type)
    record = ProjectFile(
        project_id=project_id,
        owner_id=current_user.id,
        file_name=upload.filename or Path(path).name,
        file_type=content_type,
        storage_path=path,
        file_size=size,
        extracted_text=extracted,
        summary=extracted[:1000],
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("/{project_id}")
def list_files(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    get_project(db, project_id, current_user.id)
    files = db.scalars(
        select(ProjectFile).where(ProjectFile.project_id == project_id, ProjectFile.owner_id == current_user.id)
    ).all()
    return {"items": files}


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(file_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = get_file(db, file_id, current_user.id)
    db.delete(record)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/analyze/{file_id}")
def analyze_file(file_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = get_file(db, file_id, current_user.id)
    extracted = extract_text_from_file(record.storage_path, record.file_type)
    record.extracted_text = extracted
    record.summary = extracted[:1000]
    db.commit()
    db.refresh(record)
    return record
