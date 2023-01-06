from unittest.mock import patch, Mock

import pytest

from src.modules.polls.data.datasources.poll_answer import PollAnswerMemoryDataSource
from src.modules.polls.data.datasources.poll_question import (
    PollMemoryDataSource,
    PollRetrieveDataSourceException,
)
from src.modules.polls.data.serializer import PollSerializer
from src.modules.polls.domain.poll_user_cases import (
    PollListUserCase,
    PollRetrieveUserCase,
    PollCreateUserCase,
    PollUpdateUserCase,
    PollDeleteUserCase,
)
from tests.unit.modules.polls.domain.fixtures import (
    POLL,
    POLL_ANSWER,
    POLLS,
    POLL_ANSWERS,
    CREATE_PAYLOAD,
    POLL_WITH_ANSWERS,
)


class TestListPollsUseCase:
    @patch.object(PollMemoryDataSource, "get", return_value=POLLS)
    def test_success(self, _get_mock: Mock):
        assert PollListUserCase().execute() == POLLS


class TestRetrievePollsUseCase:
    @patch.object(
        PollAnswerMemoryDataSource, "get_by_poll_id", return_value=POLL_ANSWERS
    )
    @patch.object(PollMemoryDataSource, "retrieve", return_value=POLL)
    def test_success(self, _retrieve_mock: Mock, _get_by_poll_id_answers: Mock):
        assert PollRetrieveUserCase().execute(POLL.id) == POLL_WITH_ANSWERS

    @patch.object(
        PollMemoryDataSource, "retrieve", side_effect=PollRetrieveDataSourceException()
    )
    def test_error(self, _retrieve_mock: Mock):
        with pytest.raises(PollRetrieveDataSourceException):
            PollRetrieveUserCase().execute(POLL.id)


class TestCreatePollsUseCase:
    @patch.object(PollAnswerMemoryDataSource, "create_bulk", return_value=POLL_ANSWERS)
    @patch.object(PollMemoryDataSource, "create", return_value=POLL)
    def test_success(self, _create_mock: Mock, _create_answers: Mock):
        assert PollCreateUserCase().execute(CREATE_PAYLOAD) == POLL_WITH_ANSWERS


class TestUpdatePollsUseCase:
    @patch.object(PollMemoryDataSource, "update", return_value=POLL)
    def test_success(self, _update_mock: Mock):
        assert (
            PollUpdateUserCase().execute(
                POLL.id, PollSerializer(question=POLL.question)
            )
            == POLL
        )

    @patch.object(
        PollMemoryDataSource, "update", side_effect=PollRetrieveDataSourceException()
    )
    def test_error(self, _update_mock: Mock):
        with pytest.raises(PollRetrieveDataSourceException):
            PollUpdateUserCase().execute(
                POLL.id, PollSerializer(question=POLL.question)
            )


class TestDeletePollsUseCase:
    @patch.object(PollAnswerMemoryDataSource, "delete_by_poll_id", return_value=None)
    @patch.object(PollMemoryDataSource, "delete", return_value=None)
    def test_success(self, _delete_mock: Mock, _delete_answers: Mock):
        assert PollDeleteUserCase().execute(POLL.id) is None
