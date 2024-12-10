from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from unigate.core.config import settings
from unigate.routes import auth, group, requests, student

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
def hello() -> dict[str, str]:
    return {"message": "Hello, World!"}


@app.get("/ping")
def ping() -> dict[str, str]:
    return {"message": "pong"}


app.include_router(auth.router, prefix="/auth")
app.include_router(student.router, prefix="/students")
app.include_router(group.router, prefix="/groups")
app.include_router(requests.router, prefix="/requests")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
