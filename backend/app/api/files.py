from pathlib import Path
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.config.settings import settings
from app.database.connection import get_db
from app.models.user import User
from app.models.workspace import ProjectFile
from app.services import stage1_service, usage_service
from app.services.workspace_service import delete_owned_upload, get_file, get_owned_project, get_project
from app.utils.file_processing import parse_uploaded_file, validate_upload_name

router = APIRouter(prefix="/api/files", tags=["Files"])


def _unique_upload_path(upload_dir: Path, safe_name: str) -> Path:
    original = Path(safe_name)
    stem = original.stem[:80] or "upload"
    return upload_dir / f"{stem}-{uuid.uuid4().hex[:12]}{original.suffix.lower()}"


def save_upload(user_id: int, project_id: int, upload: UploadFile) -> tuple[Path, Path, str, int]:
    try:
        safe_name = validate_upload_name(upload.filename or "upload.bin")
    except ValueError as exc:
        raise HTTPException(status_code=415, detail=str(exc)) from exc
    upload_dir = Path(settings.upload_dir) / str(user_id) / str(project_id)
    upload_dir.mkdir(parents=True, exist_ok=True)
    target = _unique_upload_path(upload_dir, safe_name)
    temp_target = upload_dir / f".{target.name}.tmp"
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    total = 0
    try:
        with temp_target.open("wb") as handle:
            while chunk := upload.file.read(1024 * 1024):
                total += len(chunk)
                if total > max_bytes:
                    raise HTTPException(status_code=413, detail="File exceeds upload limit")
                handle.write(chunk)
    except Exception:
        temp_target.unlink(missing_ok=True)
        raise
    return temp_target, target, safe_name, total


@router.post("/upload/{project_id}", status_code=status.HTTP_201_CREATED)
def upload_file(project_id: int, upload: UploadFile = File(...), db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    get_owned_project(db, project_id, current_user.id)
    temp_path, target_path, safe_name, size = save_upload(current_user.id, project_id, upload)
    try:
        usage_service.assert_storage_limit(db, current_user, size)
        temp_path.replace(target_path)
    except Exception:
        temp_path.unlink(missing_ok=True)
        raise
    content_type = upload.content_type or "application/octet-stream"
    try:
        parsed = parse_uploaded_file(str(target_path), content_type)
    except Exception as exc:
        target_path.unlink(missing_ok=True)
        raise HTTPException(status_code=422, detail=f"File could not be parsed: {exc}") from exc
    record = ProjectFile(
        project_id=project_id,
        owner_id=current_user.id,
        file_name=safe_name,
        file_type=content_type,
        storage_path=str(target_path),
        file_size=size,
        extracted_text=parsed["text"],
        summary=parsed["summary"],
    )
    db.add(record)
    db.flush()
    stage1_service.save_memory(
        db,
        project_id,
        current_user.id,
        f"file:{record.id}:{content_type}",
        str(parsed),
    )
    db.commit()
    db.refresh(record)
    return _file_response(record)


@router.get("/{project_id}")
def list_files(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    get_project(db, project_id, current_user.id)
    files = db.scalars(
        select(ProjectFile).where(ProjectFile.project_id == project_id, ProjectFile.owner_id == current_user.id)
    ).all()
    return {"items": [_file_response(file_record) for file_record in files]}


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(file_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    record = get_file(db, file_id, current_user.id)
    delete_owned_upload(record.storage_path)
    db.delete(record)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/analyze/{file_id}")
def analyze_file(file_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    result = stage1_service.analyze_project_file(db, file_id, current_user)
    result["file"] = _file_response(result["file"])
    return result


@router.post("/{file_id}/analyze-video")
def analyze_video(file_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return stage1_service.analyze_video_file(db, file_id, current_user)


def _file_response(record: ProjectFile) -> dict:
    return {
        "id": record.id,
        "project_id": record.project_id,
        "owner_id": record.owner_id,
        "file_name": record.file_name,
        "file_type": record.file_type,
        "file_size": record.file_size,
        "summary": record.summary,
        "created_at": record.created_at,
        "updated_at": record.updated_at,
    }
