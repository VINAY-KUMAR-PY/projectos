from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.connection import get_db
from app.models.user import User
from app.models.workspace import GeneratedOutput
from app.schemas.platform_schema import OutputCreate, OutputExportRequest
from app.services.workspace_service import get_owned_project, get_project

router = APIRouter(prefix="/api/outputs", tags=["Outputs"])


def get_owned_output(db: Session, output_id: int, owner_id: int):
    output = db.scalar(
        select(GeneratedOutput).where(
            GeneratedOutput.id == output_id,
            GeneratedOutput.owner_id == owner_id,
        )
    )
    if not output:
        raise HTTPException(status_code=404, detail="Output not found")
    return output


@router.post("", status_code=status.HTTP_201_CREATED)
def create_output(request: OutputCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    get_owned_project(db, request.project_id, current_user.id)
    output = GeneratedOutput(owner_id=current_user.id, **request.model_dump())
    db.add(output)
    db.commit()
    db.refresh(output)
    return output


@router.get("/{project_id}")
def list_outputs(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    get_project(db, project_id, current_user.id)
    return {"items": db.scalars(select(GeneratedOutput).where(GeneratedOutput.project_id == project_id, GeneratedOutput.owner_id == current_user.id)).all()}


@router.get("/item/{output_id}")
def get_output(output_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_owned_output(db, output_id, current_user.id)


@router.post("/{output_id}/export")
def export_output(output_id: int, request: OutputExportRequest, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    output = get_owned_output(db, output_id, current_user.id)
    return {"output_id": output.id, "format": request.format, "content": output.content}


@router.delete("/{output_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_output(output_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    output = get_owned_output(db, output_id, current_user.id)
    db.delete(output)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
