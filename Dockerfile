#Pull base image
FROM python:3.6

#Set environment variables 
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#Set work directory
WORKDIR /task

#Install dependencies 
COPY Pipfile Pipfile.lock requirements.txt /task/
RUN pip install pipenv && pipenv install --system
# RUN pipenv install -r requirements.txt

#Copy project
COPY . /task/
# RUN --name collab_db -e POSTGRES_PASSWORD=root -d postgres
