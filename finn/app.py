from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware

from finn.routes.user import router as user_router
from finn.schemas.base_schema import Message

app = FastAPI()

app.include_router(user_router)
app.add_middleware(
    CORSMiddleware,
    allowed_origins=["*"],
    allowed_methods=["*"],
    allowed_headers=["*"],
    allow_credentials=True,
)


@app.get(
    "/hello",
    status_code=status.HTTP_200_OK,
    response_model=Message,
)
def hello():
    return {"message": "hello world!"}
