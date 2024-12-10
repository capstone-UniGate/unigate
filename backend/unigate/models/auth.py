from unigate.models.base import AuthUserBase, DBAuthBase, UUIDBase


class AuthUser(DBAuthBase, UUIDBase, AuthUserBase, table=True):
    __tablename__ = "users"  # type: ignore
