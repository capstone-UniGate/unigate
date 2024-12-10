from unigate import crud
from unigate.core.database import get_session, get_auth_session
from unigate.models.group import GroupType
from unigate.schemas.group import GroupCreate
from unigate.schemas.student import StudentCreate
from unigate.schemas.auth import AuthUserCreate
from unigate.core.security import get_password_hash

students = [
    StudentCreate(
        number=4891185,
        email="s4891185@studenti.unige.it",
        name="Fabio",
        surname="Fontana",
    )
]

groups = [
    GroupCreate(
        name="Test Public Group",
        description="This is a test group",
        category="Test",
        type=GroupType.PUBLIC,
    ),
    GroupCreate(
        name="Test Private Group",
        description="This is a test group",
        category="Test",
        type=GroupType.PRIVATE,
    ),
]

users: list[AuthUserCreate] = []
for user in students:
    hashed_password = get_password_hash("testpassword")
    users.append(AuthUserCreate.model_validate(user, update={"hashed_password": hashed_password}))


def seed_auth() -> None:
    session = next(get_auth_session())
    for user in users:
        crud.auth_user.create(obj_in=user, db_session=session)

def seed_unigate() -> None:
    session = next(get_session())
    for student in students:
        current_student = crud.student.create(obj_in=student, db_session=session)
        for group in groups:
            crud.group.create(obj_in=group, update={"creator_id": current_student.id}, db_session=session)


if __name__ == "__main__":
    seed_auth()
    seed_unigate()
