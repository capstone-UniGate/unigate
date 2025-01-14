"""Add group tags

Revision ID: 92ed55d9c33a
Revises: f097df941a9f
Create Date: 2025-01-13 12:36:34.292286

"""
from collections.abc import Sequence
from sqlalchemy.dialects.postgresql import ARRAY
import sqlalchemy as sa

# see https://stackoverflow.com/a/69063829 for sqlmodel
import sqlmodel
import sqlmodel.sql.sqltypes  # noqa: F401
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '92ed55d9c33a'
down_revision: str | None = 'f097df941a9f'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("groups", sa.Column("tags", ARRAY(sa.String), nullable=True))


def downgrade() -> None:
    op.drop_column("groups", "tags")
