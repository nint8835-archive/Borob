FROM python:3
COPY . /app
WORKDIR /app
RUN apt-get install libmagickwand-dev && pip install -r requirements.txt
CMD python Bot.py