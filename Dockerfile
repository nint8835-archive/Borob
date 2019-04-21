FROM python:3-alpine
COPY . /app
WORKDIR /app
RUN apk install imagemagick-dev && pip install -r requirements.txt
CMD python Bot.py