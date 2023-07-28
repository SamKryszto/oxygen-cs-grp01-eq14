FROM python:3.11-alpine

RUN pip install pipenv

WORKDIR /usr/src/app

COPY . .

RUN pipenv install --dev

CMD [ "pipenv", "run", "start" ]
