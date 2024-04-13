FROM python:3.11

WORKDIR /tdd_lab6

RUN pip install poetry

COPY pyproject.toml poetry.lock* /tdd_lab6/

COPY test.env pytest.ini ./
COPY src src
COPY tests tests

RUN poetry install --no-interaction --no-ansi

CMD ["poetry", "run", "pytest", "tests"]
