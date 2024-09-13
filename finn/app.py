from fastapi import FastAPI, status

from finn.schemas import Message

app = FastAPI()


@app.get(
    "/hello",
    status_code=status.HTTP_200_OK,
    response_model=Message,
)
def hello():
    return {"message": "hello world!"}
    