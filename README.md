# Polls API

Project to manage polls from memory

## How to start?

1. Clone the repository

```
    git clone https://github.com/bergran/polls-back
```

2. Go to the folder

```
cd polls-back
```

3. Install dependencies


```
pipenv install
```

4. Start the project

```
uvicorn main:app --reload --host 0.0.0.0
```

or

```
make launch-api
```

## Commands

This repository has a makefile with some commands configured to apply with docker:

* launch-api: install dependencies and start api
* launch-api-pro: install dependencies and start api in production mode (No reload)
* test: launch the tests
* test-nocoverage: launch the tests without coverage

## Metrics

Polls API is metricated, metrics are:

- http_request_summary: metric time (in ms) by request with method, endpoint and status code labels
