FROM debian:trixie-20260202-slim

WORKDIR /app

RUN apt update && apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    bash \
    build-essential \
 && apt clean

COPY . .

RUN python3 -m venv venv

RUN ./venv/bin/pip install --upgrade pip
RUN ./venv/bin/pip install -r requirements.txt

RUN ./venv/bin/python init_db.py

EXPOSE 6969

CMD ["./venv/bin/python", "run.py"]