FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements-docker.txt /app/requirements-docker.txt

RUN pip install --no-cache-dir -r /app/requirements-docker.txt

COPY . /app

EXPOSE 8050
EXPOSE 8088

CMD ["bash", "/app/start_services_docker.sh"]
