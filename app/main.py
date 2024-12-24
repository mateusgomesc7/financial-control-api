"""FastAPI app."""

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from app.routers import auth, incomes, members, months, users
from app.schemas.utils import Message

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(members.router)
app.include_router(months.router)
app.include_router(incomes.router)


@app.get("/", response_model=Message)
def read_root():
    """Root path."""
    return {"message": "Hello World"}
