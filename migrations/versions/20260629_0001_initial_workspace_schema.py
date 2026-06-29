"""initial workspace schema

Revision ID: 20260629_0001
Revises:
Create Date: 2026-06-29 00:00:00
"""
from alembic import op
import sqlalchemy as sa

revision = "20260629_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=True),
        sa.Column("subscription_plan", sa.String(length=50), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)

    op.create_table(
        "workspaces",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_workspaces_id"), "workspaces", ["id"], unique=False)
    op.create_index(op.f("ix_workspaces_name"), "workspaces", ["name"], unique=False)
    op.create_index(op.f("ix_workspaces_owner_id"), "workspaces", ["owner_id"], unique=False)

    op.create_table(
        "projects",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("workspace_id", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["workspace_id"], ["workspaces.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_projects_id"), "projects", ["id"], unique=False)
    op.create_index(op.f("ix_projects_owner_id"), "projects", ["owner_id"], unique=False)
    op.create_index(op.f("ix_projects_status"), "projects", ["status"], unique=False)
    op.create_index(op.f("ix_projects_title"), "projects", ["title"], unique=False)
    op.create_index(op.f("ix_projects_workspace_id"), "projects", ["workspace_id"], unique=False)

    for table_name, title_column in [
        ("tasks", "title"),
        ("notes", "title"),
        ("project_files", "file_name"),
        ("project_memories", "key"),
    ]:
        columns = [
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("project_id", sa.Integer(), nullable=False),
            sa.Column("owner_id", sa.Integer(), nullable=False),
        ]
        if table_name == "tasks":
            columns.extend([
                sa.Column("title", sa.String(length=255), nullable=False),
                sa.Column("description", sa.Text(), nullable=True),
                sa.Column("status", sa.String(length=50), nullable=True),
                sa.Column("priority", sa.String(length=50), nullable=True),
            ])
        elif table_name == "notes":
            columns.extend([
                sa.Column("title", sa.String(length=255), nullable=False),
                sa.Column("content", sa.Text(), nullable=False),
            ])
        elif table_name == "project_files":
            columns.extend([
                sa.Column("file_name", sa.String(length=255), nullable=False),
                sa.Column("file_type", sa.String(length=100), nullable=True),
                sa.Column("storage_path", sa.String(length=500), nullable=False),
                sa.Column("file_size", sa.Integer(), nullable=True),
            ])
        else:
            columns.extend([
                sa.Column("key", sa.String(length=120), nullable=False),
                sa.Column("value", sa.Text(), nullable=False),
            ])
        columns.extend([
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
            sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
            sa.PrimaryKeyConstraint("id"),
        ])
        op.create_table(table_name, *columns)
        op.create_index(op.f(f"ix_{table_name}_id"), table_name, ["id"], unique=False)
        op.create_index(op.f(f"ix_{table_name}_owner_id"), table_name, ["owner_id"], unique=False)
        op.create_index(op.f(f"ix_{table_name}_project_id"), table_name, ["project_id"], unique=False)
        op.create_index(op.f(f"ix_{table_name}_{title_column}"), table_name, [title_column], unique=False)
        if table_name == "tasks":
            op.create_index(op.f("ix_tasks_status"), "tasks", ["status"], unique=False)
            op.create_index(op.f("ix_tasks_priority"), "tasks", ["priority"], unique=False)
        if table_name == "project_files":
            op.create_index(op.f("ix_project_files_file_type"), "project_files", ["file_type"], unique=False)


def downgrade():
    for table_name, extra_indexes in [
        ("project_memories", []),
        ("project_files", ["ix_project_files_file_type"]),
        ("notes", []),
        ("tasks", ["ix_tasks_status", "ix_tasks_priority"]),
    ]:
        for index_name in extra_indexes:
            op.drop_index(index_name, table_name=table_name)
        op.drop_index(op.f(f"ix_{table_name}_project_id"), table_name=table_name)
        op.drop_index(op.f(f"ix_{table_name}_owner_id"), table_name=table_name)
        op.drop_index(op.f(f"ix_{table_name}_id"), table_name=table_name)
        if table_name == "project_files":
            op.drop_index(op.f("ix_project_files_file_name"), table_name=table_name)
        elif table_name == "project_memories":
            op.drop_index(op.f("ix_project_memories_key"), table_name=table_name)
        else:
            op.drop_index(op.f(f"ix_{table_name}_title"), table_name=table_name)
        op.drop_table(table_name)

    op.drop_index(op.f("ix_projects_workspace_id"), table_name="projects")
    op.drop_index(op.f("ix_projects_title"), table_name="projects")
    op.drop_index(op.f("ix_projects_status"), table_name="projects")
    op.drop_index(op.f("ix_projects_owner_id"), table_name="projects")
    op.drop_index(op.f("ix_projects_id"), table_name="projects")
    op.drop_table("projects")

    op.drop_index(op.f("ix_workspaces_owner_id"), table_name="workspaces")
    op.drop_index(op.f("ix_workspaces_name"), table_name="workspaces")
    op.drop_index(op.f("ix_workspaces_id"), table_name="workspaces")
    op.drop_table("workspaces")

    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_table("users")
