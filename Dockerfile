FROM python:3-alpine
COPY . /app
WORKDIR /app
RUN echo "x86" > /etc/apk/arch && apk add imagemagick-dev=6.9.6.8-r1 --repository=http://dl-cdn.alpinelinux.org/alpine/v3.5/main && echo "x86_64" > /etc/apk/arch && pip install -r requirements.txt
CMD python Bot.py