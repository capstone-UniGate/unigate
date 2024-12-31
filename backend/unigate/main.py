from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from unigate.core.config import settings
from unigate.routes import auth, group, student
from unigate import crud
from unigate.core.database import get_session
from time import sleep

app = FastAPI()

origins = ["http://localhost", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.all_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def hello() -> dict[str, str]:
    return {"message": "Hello, World!"}


@app.get("/ping")
async def ping() -> dict[str, str]:
    return {"message": "pong"}


@app.get("/reset")
def reset() -> dict[str, str]:
    try:
        with Path("/fifo").open("w") as f:
            f.write("reset\n")
        return {"message": "reset triggered"}
    except Exception:
        return {"error": "something went wrong"}

@app.get("/wait")
def wait() -> dict[str, str]:
    sleep(5)
    try:
        for _ in range(120):
            try:
                with next(get_session()) as session:
                    test_student = crud.student.get_by_number(number=1234567, session=session)
                    if test_student:
                        return {"message": "system is ready"}
            except Exception:
                pass
            sleep(1)
    except Exception:
        pass
    return {"error": "something went wrong"}


app.include_router(auth.router, prefix="/auth")
app.include_router(student.router, prefix="/students")
app.include_router(group.router, prefix="/groups")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
