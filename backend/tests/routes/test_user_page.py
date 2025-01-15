import os

from fastapi.testclient import TestClient
from minio import Minio
from unigate.core.config import settings
from unigate.enums import Mode
from unigate.main import app

client = TestClient(app)

minio = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MODE == Mode.PROD,
)

test_student_username = "S1234567"
test_student_password = "testpassword"


def authenticate_user(
    username=test_student_username, password=test_student_password
) -> dict:
    login_payload = {
        "username": username,
        "password": password,
    }
    response = client.post("/auth/login", data=login_payload)
    assert response.status_code == 200, (
        f"Failed to authenticate user: {response.json()}"
    )
    return response.json()


def fetch_user_data() -> dict:
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/students/me", headers=headers)
    assert response.status_code == 200, f"Failed to fetch user data: {response.json()}"
    return response.json()


def fetch_user_profile_picture() -> dict:
    token_data = authenticate_user()
    token = token_data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/students/propic-presigned-url", headers=headers)
    assert response.status_code == 200, (
        f"Failed to fetch user profile picture: {response.json()}"
    )
    return response.json()


def test_verify_user_profile() -> None:
    user_data = fetch_user_data()
    profile_picture = fetch_user_profile_picture()
    assert user_data["name"] == "Test Name", "Name is wrong or not displayed"
    assert user_data["surname"] == "Test Surname", "Surname is wrong or not displayed"
    assert user_data["email"] == "s1234567@studenti.unige.it", (
        "Email is wrong or not displayed"
    )
    assert "url" in profile_picture, "Profile picture URL is not available"
    assert profile_picture["url"].startswith(
        "http://localhost:9000/unigate/propics/1234567"
    ), "Profile picture URL is incorrect"


def test_minio_connection():
    try:
        buckets = minio.list_buckets()
        assert buckets, (
            "No buckets found. MinIO potrebbe non essere configurato correttamente."
        )
        print(
            f"Connesso a MinIO. Buckets disponibili: {[bucket.name for bucket in buckets]}"
        )
    except Exception as e:
        raise AssertionError(f"Errore nella connessione a MinIO: {e}")


def test_upload_to_minio_direct() -> None:
    relative_path_profile_image = "unigate/backend/tests/routes/test.jpeg"
    project_root = os.getcwd()
    path_without_last_two = os.path.dirname(os.path.dirname(project_root))
    image_path = os.path.join(path_without_last_two, relative_path_profile_image)

    bucket_name = "unigate"
    object_name = "propics/1234567"

    assert os.path.exists(image_path), f"File not found: {image_path}"

    try:
        with open(image_path, "rb") as file_data:
            minio.put_object(
                bucket_name,
                object_name,
                file_data,
                length=os.path.getsize(image_path),
                content_type="image/jpeg",
            )
    except Exception as e:
        assert False, f"Error uploading to MinIO: {e}"

    try:
        found = minio.stat_object(bucket_name, object_name)
        assert found, f"File not found on MinIO: {bucket_name}/{object_name}"
    except Exception as e:
        assert False, f"Error checking file on MinIO: {e}"
