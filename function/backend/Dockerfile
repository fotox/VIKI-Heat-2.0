FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    python3-dev \
    python3-pip \
    libffi-dev \
    build-essential \
    libssl-dev \
    libusb-1.0-0-dev \
    locales

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install RPi.GPIO

ENV TZ=Europe/Berlin

CMD ["python", "app.py"]
