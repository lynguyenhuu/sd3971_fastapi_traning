"""init database schema

Revision ID: 434366c545b7
Revises:
Create Date: 2025-08-28 12:18:44.812268

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '434366c545b7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False, unique=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("mode", sa.String(length=50), nullable=True),
        sa.Column("rating", sa.Integer(), nullable=True),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "username",
            sa.String(length=255),
            nullable=False,
            unique=True,
            index=True,
        ),
        sa.Column("first_name", sa.String(length=255), nullable=True),
        sa.Column("last_name", sa.String(length=255), nullable=True),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column(
            "is_active",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("true"),
        ),
        sa.Column(
            "is_admin",
            sa.Boolean(),
            nullable=False,
            server_default=sa.text("false"),
        ),
        sa.Column(
            "company_id",
            sa.Integer(),
            sa.ForeignKey("companies.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )

    op.create_table(
        "tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("summary", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=50), nullable=True),
        sa.Column("priority", sa.Integer(), nullable=True),
        sa.Column(
            "user_id",
            sa.Integer(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
    )

    # ---- Seed Data ----
    # Insert one default company
    op.execute(
        sa.text(
            """
            INSERT INTO companies (id, name, description, mode, rating)
            VALUES (:id, :name, :desc, :mode, :rating)
            """
        ).bindparams(
            id=1,
            name="My Company",
            desc="First company",
            mode="standard",
            rating=5,
        )
    )

    # Insert admin user linked to company 1
    op.execute(
        sa.text(
            """
            INSERT INTO users (id, name, username, first_name, last_name, hashed_password, is_active, is_admin, company_id)
            VALUES (:id, :name, :username, :first, :last, :pwd, true, true, :company_id)
            """
        ).bindparams(
            id=1,
            name="Administrator",
            username="admin",
            first="Admin",
            last="User",
            pwd="$2b$12$SSH2v9vlf4s/1jFHiQUY6OS/7ODg06QDF04FVrjbqK9Qrhv4GMnda",
            company_id=1,
        )
    )

    # Insert example task
    op.execute(
        sa.text(
            """
            INSERT INTO tasks (id, summary, description, status, priority, user_id)
            VALUES (:id, :summary, :desc, :status, :priority, :user_id)
            """
        ).bindparams(
            id=1,
            summary="First task",
            desc="This is a demo task for the admin user",
            status="open",
            priority=1,
            user_id=1,
        )
    )


def downgrade() -> None:
    op.drop_table("tasks")
    op.drop_table("users")
    op.drop_table("companies")
