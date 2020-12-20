FROM ubuntu:latest
FROM httpd:latest
FROM python:latest

WORKDIR /dockerapps/onlinechess-project

ENV PORT 8000

ENV PATH /usr/local/bin

COPY ["home/niranj/Code/onlinechess/requirements.txt", "/dockerapps/onlinechess-project/"]
RUN apt-get install python3-dev default-libmysqlclient-dev build-essential
RUN pip install -r requirements.txt

COPY ["home/niranj/Code/onlinechess/*", "/dockerapps/onlinechess/"]

CMD ["python3", "manage.py runserver"]
