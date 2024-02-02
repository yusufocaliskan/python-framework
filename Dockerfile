FROM python:3.9
WORKDIR /app

COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app

RUN cd /app/src/libs/DocReaderAI/ && pip install .

EXPOSE 3000
