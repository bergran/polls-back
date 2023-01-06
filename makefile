launch-api:
	docker-compose up runner_local

launch-api-pro:
	docker-compose up --build runner

stop:
	docker-compose stop

test:
	docker-compose run --rm runner_local pytest --cov=./src --cov-report term-missing -svv $(ATTRS)

test-nocoverage:
	docker-compose run --rm runner_local pytest  -svv $(ATTRS)
