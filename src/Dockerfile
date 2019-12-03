# Base Image
FROM python:3.7-alpine
# FROM library/postgres

# create and set working directory
RUN mkdir /src
WORKDIR /src

# Add current directory code to working directory
COPY . /src


COPY requirements.txt /src/

# RUN adduser -D mahdi
# USER mahdi
# set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8
ENV DEBIAN_FRONTEND=noninteractive 

# set project environment variables
# grab these via Python's os.environ
# these are 100% optional here
ENV PORT=8000

# Install system dependencies
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     tzdata \
#     python3-setuptools \
#     python3-pip \
#     python3-dev \
#     python3-venv \
#     git \
#     && \
#     apt-get clean && \
#     rm -rf /var/lib/apt/lists/*


# install environment dependencies
RUN pip3 install --upgrade pip 
# RUN pip3 install pipenv

# Install project dependencies
RUN apk add --no-cache python3-dev openssl-dev libffi-dev gcc postgresql-libs postgresql-dev musl-dev git && pip3 install --upgrade pip
# RUN apk update && apk add postgresql-dev musl-dev python3-venv git
RUN apk add libjpeg
RUN apk add --no-cache jpeg-dev zlib-dev
RUN apk add --no-cache --virtual .build-deps build-base linux-headers \
    && pip install Pillow
RUN pip install -r requirements.txt
# RUN pipenv install --skip-lock --system --dev

# EXPOSE 8888
CMD gunicorn advance_blog.wsgi:application --bind 0.0.0.0:$PORT & celery worker --app=advance_blog.tasks
# CMD gunicorn /src/advance_blog.wsgi:application --bind 0.0.0.0:$PORT