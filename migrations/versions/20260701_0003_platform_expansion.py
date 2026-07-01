"""platform expansion

Revision ID: 20260701_0003
Revises: 20260629_0002
Create Date: 2026-07-01 00:00:00
"""
from alembic import op
import sqlalchemy as sa

revision = "20260701_0003"
down_revision = "20260629_0002"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("projects", sa.Column("tech_stack", sa.Text(), nullable=True))
    op.add_column("projects", sa.Column("deadline", sa.DateTime(timezone=True), nullable=True))
    op.add_column("projects", sa.Column("progress_score", sa.Integer(), nullable=True))

    op.add_column("tasks", sa.Column("assigned_to", sa.Integer(), nullable=True))
    op.add_column("tasks", sa.Column("due_date", sa.DateTime(timezone=True), nullable=True))

    op.add_column("project_files", sa.Column("extracted_text", sa.Text(), nullable=True))
    op.add_column("project_files", sa.Column("summary", sa.Text(), nullable=True))

    op.add_column("agent_runs", sa.Column("agent_name", sa.String(length=120), nullable=True))
    op.add_column("agent_runs", sa.Column("task_type", sa.String(length=120), nullable=True))
    op.add_column("agent_runs", sa.Column("input_data", sa.Text(), nullable=True))
    op.add_column("agent_runs", sa.Column("output_data", sa.Text(), nullable=True))
    op.add_column("agent_runs", sa.Column("duration_seconds", sa.Integer(), nullable=True))
    op.add_column("agent_runs", sa.Column("confidence", sa.Integer(), nullable=True))
    op.create_index(op.f("ix_agent_runs_agent_name"), "agent_runs", ["agent_name"], unique=False)
    op.create_index(op.f("ix_agent_runs_task_type"), "agent_runs", ["task_type"], unique=False)

    op.create_table(
        "generated_outputs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("output_type", sa.String(length=100), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("format", sa.String(length=50), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_generated_outputs_id"), "generated_outputs", ["id"], unique=False)
    op.create_index(op.f("ix_generated_outputs_owner_id"), "generated_outputs", ["owner_id"], unique=False)
    op.create_index(op.f("ix_generated_outputs_output_type"), "generated_outputs", ["output_type"], unique=False)
    op.create_index(op.f("ix_generated_outputs_project_id"), "generated_outputs", ["project_id"], unique=False)

    op.create_table(
        "subscriptions",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("plan", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("stripe_subscription_id", sa.String(length=255), nullable=True),
        sa.Column("current_period_start", sa.DateTime(timezone=True), nullable=True),
        sa.Column("current_period_end", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_subscriptions_id"), "subscriptions", ["id"], unique=False)
    op.create_index(op.f("ix_subscriptions_user_id"), "subscriptions", ["user_id"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_subscriptions_user_id"), table_name="subscriptions")
    op.drop_index(op.f("ix_subscriptions_id"), table_name="subscriptions")
    op.drop_table("subscriptions")
    op.drop_index(op.f("ix_generated_outputs_project_id"), table_name="generated_outputs")
    op.drop_index(op.f("ix_generated_outputs_output_type"), table_name="generated_outputs")
    op.drop_index(op.f("ix_generated_outputs_owner_id"), table_name="generated_outputs")
    op.drop_index(op.f("ix_generated_outputs_id"), table_name="generated_outputs")
    op.drop_table("generated_outputs")
    op.drop_index(op.f("ix_agent_runs_task_type"), table_name="agent_runs")
    op.drop_index(op.f("ix_agent_runs_agent_name"), table_name="agent_runs")
    op.drop_column("agent_runs", "confidence")
    op.drop_column("agent_runs", "duration_seconds")
    op.drop_column("agent_runs", "output_data")
    op.drop_column("agent_runs", "input_data")
    op.drop_column("agent_runs", "task_type")
    op.drop_column("agent_runs", "agent_name")
    op.drop_column("project_files", "summary")
    op.drop_column("project_files", "extracted_text")
    op.drop_column("tasks", "due_date")
    op.drop_column("tasks", "assigned_to")
    op.drop_column("projects", "progress_score")
    op.drop_column("projects", "deadline")
    op.drop_column("projects", "tech_stack")
