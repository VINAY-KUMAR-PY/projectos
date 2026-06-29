from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Pagination(BaseModel):
    total: int
    limit: int
    offset: int


class PaginatedResponse(BaseModel):
    items: list
    pagination: Pagination


class WorkspaceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=2000)


class WorkspaceUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=2000)


class WorkspaceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime


class ProjectCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=4000)
    status: str = Field(default="draft", min_length=1, max_length=50)


class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=4000)
    status: Optional[str] = Field(default=None, min_length=1, max_length=50)


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    workspace_id: int
    owner_id: int
    title: str
    description: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=4000)
    status: str = Field(default="todo", min_length=1, max_length=50)
    priority: str = Field(default="medium", min_length=1, max_length=50)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=4000)
    status: Optional[str] = Field(default=None, min_length=1, max_length=50)
    priority: Optional[str] = Field(default=None, min_length=1, max_length=50)


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    owner_id: int
    title: str
    description: Optional[str]
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1, max_length=20000)


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    content: Optional[str] = Field(default=None, min_length=1, max_length=20000)


class NoteResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    owner_id: int
    title: str
    content: str
    created_at: datetime
    updated_at: datetime


class FileCreate(BaseModel):
    file_name: str = Field(min_length=1, max_length=255)
    file_type: Optional[str] = Field(default=None, max_length=100)
    storage_path: str = Field(min_length=1, max_length=500)
    file_size: int = Field(default=0, ge=0)


class FileUpdate(BaseModel):
    file_name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    file_type: Optional[str] = Field(default=None, max_length=100)
    storage_path: Optional[str] = Field(default=None, min_length=1, max_length=500)
    file_size: Optional[int] = Field(default=None, ge=0)


class FileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    owner_id: int
    file_name: str
    file_type: Optional[str]
    storage_path: str
    file_size: int
    created_at: datetime
    updated_at: datetime


class MemoryCreate(BaseModel):
    key: str = Field(min_length=1, max_length=120)
    value: str = Field(min_length=1, max_length=20000)


class MemoryUpdate(BaseModel):
    key: Optional[str] = Field(default=None, min_length=1, max_length=120)
    value: Optional[str] = Field(default=None, min_length=1, max_length=20000)


class MemoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    owner_id: int
    key: str
    value: str
    created_at: datetime
    updated_at: datetime
