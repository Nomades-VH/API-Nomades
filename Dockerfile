FROM python:3.10.0
WORKDIR /app
COPY /app .
COPY /bootstrap .
COPY /general_enum .
COPY /ports .
COPY main.py .
COPY requirements.txt .
COPY Dockerfile .
RUN python -m pip install -r requirements.txt
CMD ["python", "main.py"]
EXPOSE 8000