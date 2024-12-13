"""new blocks

Revision ID: 900229402c58
Revises: d8abe333b20a
Create Date: 2024-12-13 18:25:31.606976

"""
from collections.abc import Sequence

import sqlalchemy as sa

# see https://stackoverflow.com/a/69063829 for sqlmodel
import sqlmodel
import sqlmodel.sql.sqltypes  # noqa: F401
from alembic import op


# revision identifiers, used by Alembic.
revision: str = '900229402c58'
down_revision: str | None = 'd8abe333b20a'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blocks',
    sa.Column('student_id', sa.Uuid(), nullable=False),
    sa.Column('group_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['groups.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['student_id'], ['students.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('student_id', 'group_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blocks')
    # ### end Alembic commands ###
