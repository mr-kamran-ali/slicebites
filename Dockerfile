
# BUILDING:
# docker build -t slicebites:latest .

# RUNNING:
# docker run -p 8000:8000 -t slicebites:latest

# Pull base image
FROM python:3.8-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app
ENV DB_HOST host.docker.internal
ENV DB_NAME postgres
ENV DB_PORT 5432
ENV DB_PW test
ENV DB_USER postgres

# Set work directory
WORKDIR /app

# Install postgresql libs
# RUN sed -i "/^# deb.*multiverse/ s/^# //" /etc/apt/sources.list && sed -i "/^# deb.*universe/ s/^# //" /etc/apt/sources.list && apt-get -y update && apt-get install -y software-properties-common && apt-get -y update &&  apt update && apt-get install wget
RUN apt-get -y update
RUN apt-get -y install libpq-dev python-dev gcc vmtouch

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

EXPOSE 8000
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]

