FROM python:3.10-alpine

MAINTAINER Anton Grigoryev <grianton535@gmail.com>

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ .

CMD ["python", "-m", "kachan_bot"]