FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-tk \
    tk-dev \
    tcl-dev \
    libtk8.6 \
    libtcl8.6 \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

ENV DB_HOST=db
ENV DB_NAME=db
ENV DB_USER=postgres
ENV DB_PASS=postgres
ENV DB_PORT=5432
ENV DISPLAY=host.docker.internal:0.0

CMD ["python", "app/main.py"]