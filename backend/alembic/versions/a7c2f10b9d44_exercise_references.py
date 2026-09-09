"""exercise_references table

Revision ID: a7c2f10b9d44
Revises: 5b4f85af1dfd
Create Date: 2026-09-09

Outbound authoritative references per exercise (official demonstration pages).
We link to source media, never re-host it (DECISIONS.md D7).
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a7c2f10b9d44'
down_revision: Union[str, Sequence[str], None] = '5b4f85af1dfd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "exercise_references",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "exercise_id",
            sa.Integer(),
            sa.ForeignKey("exercises.id", ondelete="CASCADE"),
            nullable=False, index=True,
        ),
        sa.Column(
            "source_id",
            sa.Integer(),
            sa.ForeignKey("sources.id"),
            nullable=True, index=True,
        ),
        sa.Column("label", sa.String(300), nullable=False),
        sa.Column("url", sa.String(800), nullable=False),
        sa.Column("kind", sa.String(30), nullable=False, server_default="program"),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True),
            nullable=False, server_default=sa.text("now()"),
        ),
        sa.UniqueConstraint("exercise_id", "url", name="uq_exercise_reference_url"),
    )


def downgrade() -> None:
    op.drop_table("exercise_references")
