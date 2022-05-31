FROM python:3.10.0
WORKDIR .
COPY . .
RUN python -m pip install -r requirements.txt
CMD ["python", "main.py"]
EXPOSE 8000