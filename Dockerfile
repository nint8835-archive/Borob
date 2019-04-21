FROM python:3-alpine
COPY . /app
WORKDIR /app
RUN apk add imagemagick-dev=6.9.6.8-r1 --repository=http://dl-cdn.alpinelinux.org/alpine/v3.5/main && pip install -r requirements.txt
CMD python Bot.py