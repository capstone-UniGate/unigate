from typing import TYPE_CHECKING

from sqlmodel import Relationship

from unigate.models.base import AuthUserBase, DBAuthBase, UUIDBase
from unigate.models.teach import Teach

if TYPE_CHECKING:
    from unigate.models.course import Course


class AuthUser(DBAuthBase, UUIDBase, AuthUserBase, table=True):
    __tablename__ = "users"  # type: ignore

    courses: list["Course"] = Relationship(
        back_populates="professors", link_model=Teach
    )
