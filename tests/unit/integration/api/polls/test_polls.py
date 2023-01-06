from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.modules.polls.data.datasources.poll_question import PollMemoryDataSource
from src.modules.polls.presentation.views import api_router
from tests.unit.integration.api.polls.fixtures import (
    RESPONSE_POLLS,
    POLL,
    RESPONSE_RETRIEVE_POLL,
    PAYLOAD_UPDATED_POLL,
    PAYLOAD_REQUEST_UPDATED_POLL,
    PAYLOAD_CREATED_POLL,
)

app = FastAPI()
app.include_router(api_router)
client = TestClient(app)


class TestListPolls:
    ENDPOINT = "/polls/"

    def test_list(self, polls: PollMemoryDataSource):
        response = client.get(self.ENDPOINT)

        assert response.status_code == 200
        assert response.json() == RESPONSE_POLLS


class TestCreatePolls:
    ENDPOINT = "/polls/"

    def test_success(self, polls: PollMemoryDataSource):
        response = client.post(self.ENDPOINT, json=PAYLOAD_REQUEST_UPDATED_POLL)
        assert response.status_code == 200
        assert response.json() == PAYLOAD_CREATED_POLL


class TestRetrievePolls:
    ENDPOINT = "/polls/{}/"

    def test_success(self, polls: PollMemoryDataSource):
        response = client.get(self.ENDPOINT.format(POLL.id))

        assert response.status_code == 200
        assert response.json() == RESPONSE_RETRIEVE_POLL

    def test_error(self, polls: PollMemoryDataSource):
        response = client.get(self.ENDPOINT.format("no-exists"))

        assert response.status_code == 404


class TestUpdatePolls:
    ENDPOINT = "/polls/{}/"

    def test_success(self, polls: PollMemoryDataSource):
        response = client.put(
            self.ENDPOINT.format(POLL.id), json=PAYLOAD_REQUEST_UPDATED_POLL
        )
        assert response.status_code == 200
        assert response.json() == PAYLOAD_UPDATED_POLL

    def test_error(self, polls: PollMemoryDataSource):
        response = client.put(
            self.ENDPOINT.format("no-exists"), json=PAYLOAD_REQUEST_UPDATED_POLL
        )

        assert response.status_code == 404


class TestDeletePolls:
    ENDPOINT = "/polls/{}/"

    def test_success(self, polls: PollMemoryDataSource):
        response = client.delete(self.ENDPOINT.format(POLL.id))

        assert response.status_code == 204

    def test_error(self, polls: PollMemoryDataSource):
        response = client.delete(self.ENDPOINT.format("no-exists"))

        assert response.status_code == 204
