"""FastAPI app."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.modules.auth.routers import router as auth_router
from app.modules.essential_expense.routers import (
    router as essential_expense_router,
)
from app.modules.income.routers import router as income_router
from app.modules.member.routers import router as member_router
from app.modules.month.routers import router as month_router
from app.modules.non_essential_expense.routers import (
    router as non_essential_expense_router,
)
from app.modules.user.routers import router as user_router
from app.shared.schemas.utils import Message

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(member_router)
app.include_router(month_router)
app.include_router(income_router)
app.include_router(essential_expense_router)
app.include_router(non_essential_expense_router)


@app.get("/", response_model=Message)
def read_root():
    """Root path."""
    return {"message": "Hello World"}
