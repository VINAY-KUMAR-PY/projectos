"""ai core tables

Revision ID: 20260629_0002
Revises: 20260629_0001
Create Date: 2026-06-29 00:00:00
"""
from alembic import op
import sqlalchemy as sa

revision = "20260629_0002"
down_revision = "20260629_0001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "conversations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_conversations_id"), "conversations", ["id"], unique=False)
    op.create_index(op.f("ix_conversations_owner_id"), "conversations", ["owner_id"], unique=False)
    op.create_index(op.f("ix_conversations_project_id"), "conversations", ["project_id"], unique=False)

    op.create_table(
        "conversation_messages",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("conversation_id", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversations.id"]),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_conversation_messages_conversation_id"), "conversation_messages", ["conversation_id"], unique=False)
    op.create_index(op.f("ix_conversation_messages_id"), "conversation_messages", ["id"], unique=False)
    op.create_index(op.f("ix_conversation_messages_owner_id"), "conversation_messages", ["owner_id"], unique=False)
    op.create_index(op.f("ix_conversation_messages_role"), "conversation_messages", ["role"], unique=False)

    op.create_table(
        "agent_runs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.Column("conversation_id", sa.Integer(), nullable=True),
        sa.Column("agent_id", sa.String(length=120), nullable=False),
        sa.Column("provider", sa.String(length=80), nullable=False),
        sa.Column("model", sa.String(length=120), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("output", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("input_tokens", sa.Integer(), nullable=True),
        sa.Column("output_tokens", sa.Integer(), nullable=True),
        sa.Column("estimated_cost_inr", sa.Integer(), nullable=True),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversations.id"]),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_agent_runs_agent_id"), "agent_runs", ["agent_id"], unique=False)
    op.create_index(op.f("ix_agent_runs_conversation_id"), "agent_runs", ["conversation_id"], unique=False)
    op.create_index(op.f("ix_agent_runs_id"), "agent_runs", ["id"], unique=False)
    op.create_index(op.f("ix_agent_runs_owner_id"), "agent_runs", ["owner_id"], unique=False)
    op.create_index(op.f("ix_agent_runs_project_id"), "agent_runs", ["project_id"], unique=False)
    op.create_index(op.f("ix_agent_runs_provider"), "agent_runs", ["provider"], unique=False)
    op.create_index(op.f("ix_agent_runs_status"), "agent_runs", ["status"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_agent_runs_status"), table_name="agent_runs")
    op.drop_index(op.f("ix_agent_runs_provider"), table_name="agent_runs")
    op.drop_index(op.f("ix_agent_runs_project_id"), table_name="agent_runs")
    op.drop_index(op.f("ix_agent_runs_owner_id"), table_name="agent_runs")
    op.drop_index(op.f("ix_agent_runs_id"), table_name="agent_runs")
    op.drop_index(op.f("ix_agent_runs_conversation_id"), table_name="agent_runs")
    op.drop_index(op.f("ix_agent_runs_agent_id"), table_name="agent_runs")
    op.drop_table("agent_runs")

    op.drop_index(op.f("ix_conversation_messages_role"), table_name="conversation_messages")
    op.drop_index(op.f("ix_conversation_messages_owner_id"), table_name="conversation_messages")
    op.drop_index(op.f("ix_conversation_messages_id"), table_name="conversation_messages")
    op.drop_index(op.f("ix_conversation_messages_conversation_id"), table_name="conversation_messages")
    op.drop_table("conversation_messages")

    op.drop_index(op.f("ix_conversations_project_id"), table_name="conversations")
    op.drop_index(op.f("ix_conversations_owner_id"), table_name="conversations")
    op.drop_index(op.f("ix_conversations_id"), table_name="conversations")
    op.drop_table("conversations")
