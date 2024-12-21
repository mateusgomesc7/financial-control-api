"""FastAPI app."""

from fastapi import FastAPI

from app.routers import auth, members, users
from app.schemas.utils import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(members.router)


@app.get("/", response_model=Message)
def read_root():
    """Root path."""
    return {"message": "Hello World"}
