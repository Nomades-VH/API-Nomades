FROM python:3.10

WORKDIR /usr/src/app/

COPY . .

RUN python -m pip install poetry
RUN poetry install

EXPOSE 8000

CMD ["poetry", "run", "python", "main.py"]
