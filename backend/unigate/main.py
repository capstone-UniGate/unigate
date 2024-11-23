from fastapi import FastAPI

from .routes import groups  # Import the new groups router
from .routes import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def main() -> dict[str, str]:
    """Root endpoint to confirm the API is working."""
    return {"message": "Hello, World!"}


# Include the groups router under /groups
app.include_router(groups.router, prefix="/groups")
app.include_router(requests.router, prefix="/requests")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8080)
