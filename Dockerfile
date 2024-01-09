FROM python:3.10-slim

WORKDIR /usr/src/app

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY ./app/. .

CMD [ "python", "-m", "flask", "--app", "app", "run", "--host=0.0.0.0" ]
