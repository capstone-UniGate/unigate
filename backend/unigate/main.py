from fastapi import APIRouter, FastAPI

app = FastAPI()


@app.get("/")
def main() -> dict[str, str]:
    return {"message": "Hello, World!"}


router = APIRouter()

# define routers inside the routers folder and add them here
app.include_router(router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
