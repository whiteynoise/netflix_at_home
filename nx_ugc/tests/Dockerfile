FROM python:3.9-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt
COPY ../ /app/

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

ENV PYTHONPATH=/app/src

CMD ["pytest", "-v /app/tests/src/", "--disable-warnings", "-v"]
