FROM python:3.8-slim-buster

COPY . /usr/src/taxi-api

WORKDIR /usr/src/taxi-api
RUN pip install --no-cache -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "main:app"]
