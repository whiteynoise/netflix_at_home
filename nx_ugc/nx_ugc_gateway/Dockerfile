FROM python:3.10

WORKDIR /app

COPY ./nx_ugc_gateway/requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY ./nx_ugc_gateway/src /app/src
COPY ./commons /app/src/commons

ENV PYTHONPATH=/app/src

EXPOSE 9001
