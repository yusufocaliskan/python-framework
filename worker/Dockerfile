FROM python:3.9-alpine



COPY . /worker
WORKDIR /worker

RUN pip install -U setuptools pip
RUN pip install -r requirements.txt

# hot code reloading
CMD watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- celery -A CelerySetup worker --concurrency=1 --loglevel=INFO -E
