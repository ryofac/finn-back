from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from finn.auth.router import auth_router
from finn.categories.router import category_router
from finn.debit.router import debit_router
from finn.users.router import user_router

app = FastAPI(
    title="Finn APP",
    description="API da sua aplicação de finanças",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(debit_router)
app.include_router(category_router)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
