FROM python:3.12

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    # PIP
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # POETRY
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

WORKDIR /usr/src/app/

COPY . .

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | python3 -

RUN poetry add psycopg2
RUN poetry install --no-root

EXPOSE 8000

CMD ["poetry", "run", "python", "main.py"]
