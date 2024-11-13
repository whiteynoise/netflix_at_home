FROM python:3.10

WORKDIR /opt/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY after_start_commands.sh requirements.txt ./

RUN apt-get update && apt-get install -y netcat-traditional \
    && chmod +x after_start_commands.sh \
    && pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
