from fastapi import FastAPI

from .routes import groups  # Import the new groups router

app = FastAPI()


@app.get("/")
def main() -> dict[str, str]:
    """Root endpoint to confirm the API is working."""
    return {"message": "Hello, World!"}


# Include the groups router under /groups
app.include_router(groups.router, prefix="/groups")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
