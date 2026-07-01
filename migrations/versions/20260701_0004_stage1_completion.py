"""stage1 completion tables

Revision ID: 20260701_0004
Revises: 20260701_0003
Create Date: 2026-07-01 00:00:00
"""
from alembic import op
import sqlalchemy as sa

revision = "20260701_0004"
down_revision = "20260701_0003"
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("users", sa.Column("is_2fa_enabled", sa.Boolean(), nullable=True))
    op.add_column("users", sa.Column("totp_secret", sa.String(length=64), nullable=True))

    op.create_table(
        "team_members",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_team_members_email"), "team_members", ["email"], unique=False)
    op.create_index(op.f("ix_team_members_id"), "team_members", ["id"], unique=False)
    op.create_index(op.f("ix_team_members_owner_id"), "team_members", ["owner_id"], unique=False)
    op.create_index(op.f("ix_team_members_project_id"), "team_members", ["project_id"], unique=False)
    op.create_index(op.f("ix_team_members_role"), "team_members", ["role"], unique=False)
    op.create_index(op.f("ix_team_members_status"), "team_members", ["status"], unique=False)
    op.create_index(op.f("ix_team_members_user_id"), "team_members", ["user_id"], unique=False)

    op.create_table(
        "comments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("author_id", sa.Integer(), nullable=False),
        sa.Column("entity_type", sa.String(length=50), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column("body", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["author_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_comments_author_id"), "comments", ["author_id"], unique=False)
    op.create_index(op.f("ix_comments_entity_id"), "comments", ["entity_id"], unique=False)
    op.create_index(op.f("ix_comments_entity_type"), "comments", ["entity_type"], unique=False)
    op.create_index(op.f("ix_comments_id"), "comments", ["id"], unique=False)
    op.create_index(op.f("ix_comments_owner_id"), "comments", ["owner_id"], unique=False)
    op.create_index(op.f("ix_comments_project_id"), "comments", ["project_id"], unique=False)

    op.create_table(
        "task_assignments",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("task_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("assignee_email", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("created_by", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["task_id"], ["tasks.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_task_assignments_assignee_email"), "task_assignments", ["assignee_email"], unique=False)
    op.create_index(op.f("ix_task_assignments_created_by"), "task_assignments", ["created_by"], unique=False)
    op.create_index(op.f("ix_task_assignments_id"), "task_assignments", ["id"], unique=False)
    op.create_index(op.f("ix_task_assignments_project_id"), "task_assignments", ["project_id"], unique=False)
    op.create_index(op.f("ix_task_assignments_task_id"), "task_assignments", ["task_id"], unique=False)

    op.create_table(
        "approval_requests",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.Column("output_id", sa.Integer(), nullable=False),
        sa.Column("requester_id", sa.Integer(), nullable=False),
        sa.Column("reviewer_email", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("decided_by", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["decided_by"], ["users.id"]),
        sa.ForeignKeyConstraint(["output_id"], ["generated_outputs.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["requester_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_approval_requests_id"), "approval_requests", ["id"], unique=False)
    op.create_index(op.f("ix_approval_requests_output_id"), "approval_requests", ["output_id"], unique=False)
    op.create_index(op.f("ix_approval_requests_project_id"), "approval_requests", ["project_id"], unique=False)
    op.create_index(op.f("ix_approval_requests_requester_id"), "approval_requests", ["requester_id"], unique=False)
    op.create_index(op.f("ix_approval_requests_reviewer_email"), "approval_requests", ["reviewer_email"], unique=False)
    op.create_index(op.f("ix_approval_requests_status"), "approval_requests", ["status"], unique=False)

    op.create_table(
        "marketplace_items",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("item_type", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("price_inr", sa.Integer(), nullable=False),
        sa.Column("content_ref", sa.String(length=500), nullable=False),
        sa.Column("creator_id", sa.Integer(), nullable=False),
        sa.Column("is_public", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["creator_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_marketplace_items_creator_id"), "marketplace_items", ["creator_id"], unique=False)
    op.create_index(op.f("ix_marketplace_items_id"), "marketplace_items", ["id"], unique=False)
    op.create_index(op.f("ix_marketplace_items_is_public"), "marketplace_items", ["is_public"], unique=False)
    op.create_index(op.f("ix_marketplace_items_item_type"), "marketplace_items", ["item_type"], unique=False)
    op.create_index(op.f("ix_marketplace_items_title"), "marketplace_items", ["title"], unique=False)

    op.create_table(
        "usage_records",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("project_id", sa.Integer(), nullable=True),
        sa.Column("metric", sa.String(length=80), nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column("cycle", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_usage_records_created_at"), "usage_records", ["created_at"], unique=False)
    op.create_index(op.f("ix_usage_records_cycle"), "usage_records", ["cycle"], unique=False)
    op.create_index(op.f("ix_usage_records_id"), "usage_records", ["id"], unique=False)
    op.create_index(op.f("ix_usage_records_metric"), "usage_records", ["metric"], unique=False)
    op.create_index(op.f("ix_usage_records_project_id"), "usage_records", ["project_id"], unique=False)
    op.create_index(op.f("ix_usage_records_user_id"), "usage_records", ["user_id"], unique=False)

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("action", sa.String(length=120), nullable=False),
        sa.Column("entity_type", sa.String(length=80), nullable=True),
        sa.Column("entity_id", sa.Integer(), nullable=True),
        sa.Column("detail", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_audit_logs_action"), "audit_logs", ["action"], unique=False)
    op.create_index(op.f("ix_audit_logs_created_at"), "audit_logs", ["created_at"], unique=False)
    op.create_index(op.f("ix_audit_logs_entity_id"), "audit_logs", ["entity_id"], unique=False)
    op.create_index(op.f("ix_audit_logs_entity_type"), "audit_logs", ["entity_type"], unique=False)
    op.create_index(op.f("ix_audit_logs_id"), "audit_logs", ["id"], unique=False)
    op.create_index(op.f("ix_audit_logs_user_id"), "audit_logs", ["user_id"], unique=False)

    op.create_table(
        "user_integrations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("provider", sa.String(length=80), nullable=False),
        sa.Column("external_account_id", sa.String(length=255), nullable=True),
        sa.Column("access_token", sa.Text(), nullable=True),
        sa.Column("refresh_token", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_integrations_id"), "user_integrations", ["id"], unique=False)
    op.create_index(op.f("ix_user_integrations_provider"), "user_integrations", ["provider"], unique=False)
    op.create_index(op.f("ix_user_integrations_status"), "user_integrations", ["status"], unique=False)
    op.create_index(op.f("ix_user_integrations_user_id"), "user_integrations", ["user_id"], unique=False)


def downgrade():
    op.drop_index(op.f("ix_user_integrations_user_id"), table_name="user_integrations")
    op.drop_index(op.f("ix_user_integrations_status"), table_name="user_integrations")
    op.drop_index(op.f("ix_user_integrations_provider"), table_name="user_integrations")
    op.drop_index(op.f("ix_user_integrations_id"), table_name="user_integrations")
    op.drop_table("user_integrations")
    op.drop_index(op.f("ix_audit_logs_user_id"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_id"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_entity_type"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_entity_id"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_created_at"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_action"), table_name="audit_logs")
    op.drop_table("audit_logs")
    op.drop_index(op.f("ix_usage_records_user_id"), table_name="usage_records")
    op.drop_index(op.f("ix_usage_records_project_id"), table_name="usage_records")
    op.drop_index(op.f("ix_usage_records_metric"), table_name="usage_records")
    op.drop_index(op.f("ix_usage_records_id"), table_name="usage_records")
    op.drop_index(op.f("ix_usage_records_cycle"), table_name="usage_records")
    op.drop_index(op.f("ix_usage_records_created_at"), table_name="usage_records")
    op.drop_table("usage_records")
    op.drop_index(op.f("ix_marketplace_items_title"), table_name="marketplace_items")
    op.drop_index(op.f("ix_marketplace_items_item_type"), table_name="marketplace_items")
    op.drop_index(op.f("ix_marketplace_items_is_public"), table_name="marketplace_items")
    op.drop_index(op.f("ix_marketplace_items_id"), table_name="marketplace_items")
    op.drop_index(op.f("ix_marketplace_items_creator_id"), table_name="marketplace_items")
    op.drop_table("marketplace_items")
    op.drop_index(op.f("ix_approval_requests_status"), table_name="approval_requests")
    op.drop_index(op.f("ix_approval_requests_reviewer_email"), table_name="approval_requests")
    op.drop_index(op.f("ix_approval_requests_requester_id"), table_name="approval_requests")
    op.drop_index(op.f("ix_approval_requests_project_id"), table_name="approval_requests")
    op.drop_index(op.f("ix_approval_requests_output_id"), table_name="approval_requests")
    op.drop_index(op.f("ix_approval_requests_id"), table_name="approval_requests")
    op.drop_table("approval_requests")
    op.drop_index(op.f("ix_task_assignments_task_id"), table_name="task_assignments")
    op.drop_index(op.f("ix_task_assignments_project_id"), table_name="task_assignments")
    op.drop_index(op.f("ix_task_assignments_id"), table_name="task_assignments")
    op.drop_index(op.f("ix_task_assignments_created_by"), table_name="task_assignments")
    op.drop_index(op.f("ix_task_assignments_assignee_email"), table_name="task_assignments")
    op.drop_table("task_assignments")
    op.drop_index(op.f("ix_comments_project_id"), table_name="comments")
    op.drop_index(op.f("ix_comments_owner_id"), table_name="comments")
    op.drop_index(op.f("ix_comments_id"), table_name="comments")
    op.drop_index(op.f("ix_comments_entity_type"), table_name="comments")
    op.drop_index(op.f("ix_comments_entity_id"), table_name="comments")
    op.drop_index(op.f("ix_comments_author_id"), table_name="comments")
    op.drop_table("comments")
    op.drop_index(op.f("ix_team_members_user_id"), table_name="team_members")
    op.drop_index(op.f("ix_team_members_status"), table_name="team_members")
    op.drop_index(op.f("ix_team_members_role"), table_name="team_members")
    op.drop_index(op.f("ix_team_members_project_id"), table_name="team_members")
    op.drop_index(op.f("ix_team_members_owner_id"), table_name="team_members")
    op.drop_index(op.f("ix_team_members_id"), table_name="team_members")
    op.drop_index(op.f("ix_team_members_email"), table_name="team_members")
    op.drop_table("team_members")
    op.drop_column("users", "totp_secret")
    op.drop_column("users", "is_2fa_enabled")
