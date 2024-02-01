FROM python:3.9-slim-buster
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt
COPY . .
EXPOSE 3000
CMD ./bin/RunDevServer
# CMD env FLASK_APP=main.py python3 -m flask run -h 0.0.0.0 -p 3000
