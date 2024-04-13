FROM python:3.11

WORKDIR /tdd_lab6

RUN pip install poetry

COPY pyproject.toml poetry.lock* /tdd_lab6/

COPY .env ./
COPY src src

RUN poetry install --no-interaction --no-ansi


CMD ["poetry", "run", "uvicorn", "tdd_lab6.main:create_app", "--factory", "--reload", "--host", "0.0.0.0", "--port", "8081"]