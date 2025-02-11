"""initialize models

Revision ID: 67b7e89ce373
Revises:
Create Date: 2024-12-09 01:44:34.587314

"""

from collections.abc import Sequence

import sqlalchemy as sa

# see https://stackoverflow.com/a/69063829 for sqlmodel
import sqlmodel
import sqlmodel.sql.sqltypes
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "67b7e89ce373"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("number", sa.Integer(), nullable=False),
        sa.Column(
            "hashed_password", sqlmodel.sql.sqltypes.AutoString(), nullable=False
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_users_hashed_password"), "users", ["hashed_password"], unique=False
    )
    op.create_index(op.f("ix_users_number"), "users", ["number"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_users_number"), table_name="users")
    op.drop_index(op.f("ix_users_hashed_password"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###
