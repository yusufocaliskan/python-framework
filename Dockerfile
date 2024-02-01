FROM python:3.9
WORKDIR /app

COPY ./requirements.txt /app

RUN pip install -r requirements.txt

# Ensure all necessary files are copied before attempting to install DocReaderAI
COPY . /app

RUN cd /app/libs/DocReaderAI/ && pip install .

EXPOSE 3000
