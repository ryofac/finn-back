from fastapi import FastAPI

from finn.categories.router import category_router
from finn.debit.router import debit_router
from finn.users.router import user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(debit_router)
app.include_router(category_router)
