FROM python:3.9

WORKDIR /code
COPY poetry.lock pyproject.toml /code/

RUN pip install poetry
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /code
