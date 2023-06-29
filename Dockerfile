FROM python:3.8

RUN pip install pipenv

WORKDIR /usr/src/app

COPY . .

RUN pipenv install

CMD [ "pipenv", "run", "start" ]