"""refactor

Revision ID: ac5e578d100b
Revises: 61abd54732d3
Create Date: 2024-12-12 11:50:55.172213

"""

from collections.abc import Sequence

# see https://stackoverflow.com/a/69063829 for sqlmodel
import sqlmodel
import sqlmodel.sql.sqltypes  # noqa: F401

# revision identifiers, used by Alembic.
revision: str = "ac5e578d100b"
down_revision: str | None = "61abd54732d3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###