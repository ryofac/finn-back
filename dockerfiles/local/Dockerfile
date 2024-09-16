FROM python:3.12-alpine

WORKDIR /app

COPY ./requirements /app/requirements

RUN apk add --no-cache gcc musl-dev libffi-dev postgresql-dev

RUN pip install --no-cache-dir --upgrade -r /app/requirements/base.txt && \
    pip install --no-cache-dir -r /app/requirements/local.txt

COPY . /app

# Rodar as migrações
CMD ["echo", "Rodando migrações..."]
CMD ["alembic", "upgrade", "head"]

# Iniciar o servidor FastAPI
CMD ["echo", "Iniciando servidor migrações..."]
EXPOSE 8000

CMD ["fastapi", "dev", "finn/main.py", "--port", "8000", "--host", "0.0.0.0"]
