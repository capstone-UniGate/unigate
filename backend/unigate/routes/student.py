from datetime import timedelta

from fastapi import APIRouter, Depends
from minio import Minio

from unigate.core.config import settings
from unigate.models import Student
from unigate.routes.deps import get_current_user
from unigate.schemas.student import StudentRead, StudentReadOnlyGroups
from unigate.enums import Mode

router = APIRouter()


minio = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MODE == Mode.PROD,
)


@router.get("/me", response_model=StudentRead)
def get_me(
    current_user: Student = Depends(get_current_user(wanted_model=Student)),
) -> Student:
    return current_user


@router.get(
    "/groups",
    response_model=StudentReadOnlyGroups,
)
def get_groups(
    current_user: Student = Depends(get_current_user(wanted_model=Student)),
) -> Student:
    return current_user


@router.get(
    "/propic-presigned-url",
)
def get_propic_presigned_url(
    current_user: Student = Depends(get_current_user(wanted_model=Student)),
) -> dict[str, str]:
    presigned_url = minio.presigned_put_object(
        "unigate",
        f"propics/{current_user.number}",
        expires=timedelta(minutes=60),
    )
    return {"url": presigned_url}
