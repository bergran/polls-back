FROM python:3.10.9-slim-bullseye as builder

WORKDIR /builds

RUN pip install pipenv

COPY ./Pipfile /builds
COPY ./Pipfile.lock /builds

RUN pipenv requirements > requirements.txt

FROM python:3.10.9-slim-bullseye as runner

WORKDIR /app

COPY --from=builder /builds/requirements.txt /app
COPY ./src /app
COPY ./scripts/ /app/scripts

RUN pwd && ls && pip install -r ./requirements.txt

CMD ["bash", "./scripts/run_app.sh"]
