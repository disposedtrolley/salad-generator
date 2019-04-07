FROM python:3.7

WORKDIR /app

COPY . /app

RUN pip install pipenv
RUN pipenv install --system --deploy

CMD cd ./traversal && python __init__.py

