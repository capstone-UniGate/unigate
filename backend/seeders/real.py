from unigate import crud
from unigate.core.database import get_auth_session, get_session
from unigate.core.security import get_password_hash
from unigate.enums import GroupType
from unigate.schemas.auth import AuthUserCreate
from unigate.schemas.group import GroupCreate
from unigate.schemas.student import StudentCreate

students = [
    StudentCreate(
        number=4891185,
        email="s4891185@studenti.unige.it",
        name="Fabio",
        surname="Fontana",
    ),
    StudentCreate(
        number=4989646,
        email="s4989686@studenti.unige.it",
        name="Lorenzo",
        surname="Foschi",
    ),
    StudentCreate(
        number=5806782,
        email="s5806782@studenti.unige.it",
        name="Mimmo",
        surname="Torabi",
    ),
    StudentCreate(
        number=1234567,
        email="s1234567@studenti.unige.it",
        name="Test Name",
        surname="Test Surname",
    ),
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
    users.append(
        AuthUserCreate.model_validate(user, update={"hashed_password": hashed_password})
    )


def seed_auth() -> None:
    session = next(get_auth_session())
    for user in users:
        crud.auth_user.create(obj_in=user, session=session)


def seed_unigate() -> None:
    session = next(get_session())
    for student in students:
        current_student = crud.student.create(obj_in=student, session=session)
        for group in groups:
            group = crud.group.create(
                obj_in=group,
                update={
                    "creator_id": current_student.id,
                    "name": f"{group.name} {current_student.number}",
                },
                session=session,
            )
            group.students.append(current_student)
            group.super_students.append(current_student)
            session.add(group)
            session.commit()


if __name__ == "__main__":
    seed_auth()
    seed_unigate()
