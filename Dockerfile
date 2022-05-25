FROM python:3.10.0
WORKDIR /app
COPY . .
RUN python -m pip install -r requirements.txt
CMD ["docker start postgres"]
CMD ["docker-compose up"]
EXPOSE 80