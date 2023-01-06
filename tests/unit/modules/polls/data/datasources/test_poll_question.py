from typing import List

import pytest

from src.modules.polls.data.datasources.poll_question import (
    PollMemoryDataSource,
    PollRetrieveDataSourceException,
)
from src.modules.polls.data.models import Poll, PollRaw

POLL_1 = Poll("ba8ed951-1245-4938-8ea6-8d2980f678ce", "Poll 1")
POLL_2 = Poll("ba8ed951-1245-4938-8ea6-8d2980f678cF", "Poll 1")


def init_polls() -> List[Poll]:
    return [POLL_1, POLL_2]


class TestPollMemoryDataSource:
    def test_get(self) -> None:
        datasource = PollMemoryDataSource()
        POLLS = init_polls()
        datasource._polls = POLLS

        assert datasource.get() == POLLS

    def test_retrieve(self) -> None:
        datasource = PollMemoryDataSource()
        POLLS = init_polls()

        datasource._polls = POLLS

        assert datasource.retrieve(POLL_1.id) == POLL_1

    def test_retrieve_error(self) -> None:
        datasource = PollMemoryDataSource()

        with pytest.raises(PollRetrieveDataSourceException):
            datasource.retrieve("Error")

    def test_create(self) -> None:
        datasource = PollMemoryDataSource()
        poll = datasource.create(PollRaw(POLL_1.question))
        assert poll.question == POLL_1.question

    def test_update(self) -> None:
        datasource = PollMemoryDataSource()
        POLLS = init_polls()

        datasource._polls = POLLS

        expected_poll = PollRaw("Updated")

        assert (
            datasource.update(POLL_1.id, expected_poll).question
            == expected_poll.question
        )

    def test_update_error(self) -> None:
        datasource = PollMemoryDataSource()
        datasource._polls = []

        with pytest.raises(PollRetrieveDataSourceException):
            datasource.update(POLL_1.id, PollRaw("Updated"))

    def test_delete(self) -> None:
        datasource = PollMemoryDataSource()
        POLLS = init_polls()

        datasource._polls = POLLS

        assert datasource.delete(POLL_1.id) is None
        assert len(datasource._polls) == len(POLLS) - 1

    def test_delete_non_exists_id(self) -> None:
        datasource = PollMemoryDataSource()
        POLLS = init_polls()
        datasource._polls = POLLS

        assert datasource.delete("test") is None
        assert len(datasource._polls) == len(POLLS)
