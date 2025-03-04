FROM python:3.10-alpine

COPY ./requirements.txt .

RUN pip install --no-cache -r requirements.txt
RUN apk add --no-cache bash postgresql-client build-base postgresql-dev

COPY . .