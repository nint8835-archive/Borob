FROM python:3-alpine
COPY . /app
WORKDIR /app
RUN apk add imagemagick-dev=6.9.6.8-r1 && pip install -r requirements.txt
CMD python Bot.py