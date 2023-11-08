FROM python:3.10.0
WORKDIR /usr/src/app/
COPY . .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
CMD ["python", "main.py"]
EXPOSE 8000