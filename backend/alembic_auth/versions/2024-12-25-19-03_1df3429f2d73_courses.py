"""courses

Revision ID: 1df3429f2d73
Revises: 29e7e6f63646
Create Date: 2024-12-25 19:03:39.558248

"""

from collections.abc import Sequence

import sqlalchemy as sa

# see https://stackoverflow.com/a/69063829 for sqlmodel
import sqlmodel
import sqlmodel.sql.sqltypes
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1df3429f2d73"
down_revision: str | None = "29e7e6f63646"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "courses",
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_courses_name"), "courses", ["name"], unique=True)
    op.create_table(
        "exams",
        sa.Column("course_id", sa.Uuid(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "teaches",
        sa.Column("professor_id", sa.Uuid(), nullable=False),
        sa.Column("course_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(["course_id"], ["courses.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["professor_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("professor_id", "course_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("teaches")
    op.drop_table("exams")
    op.drop_index(op.f("ix_courses_name"), table_name="courses")
    op.drop_table("courses")
    # ### end Alembic commands ###