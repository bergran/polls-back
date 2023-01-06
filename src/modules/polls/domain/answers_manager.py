from typing import List

from src.modules.polls.data.datasources.poll_answer import (
    PollAnswerBaseDataSource,
    PollAnswerMemoryDataSource,
)
from src.modules.polls.data.datasources.poll_answer_vote import PollAnswerVoteMemoryDatasource, \
    PollAnswerVoteBaseDatasource
from src.modules.polls.data.models import PollAnswer, PollAnswerRaw, PollAnswerVotes
from src.modules.polls.data.serializer import PollAnswerSerializer


class PollAnswerStateUpdater:
    _datasource: PollAnswerBaseDataSource

    def __init__(self):
        self._datasource = PollAnswerMemoryDataSource()

    def create_bulk(
        self, poll_id: str, answers: List[PollAnswerSerializer]
    ) -> List[PollAnswer]:
        return self._datasource.create_bulk(
            [PollAnswerRaw(answer.text, poll_id) for answer in answers]
        )

    def delete_by_poll_id(self, poll_id: str) -> None:
        return self._datasource.delete_by_poll_id(poll_id)


class PollAnswerStateReader:
    _datasource: PollAnswerBaseDataSource

    def __init__(self):
        self._datasource = PollAnswerMemoryDataSource()

    def get_by_poll_id(self, poll_id: str) -> List[PollAnswer]:
        return self._datasource.get_by_poll_id(poll_id)


class PollAnswerVoteStateReader:
    _datasource: PollAnswerVoteBaseDatasource

    def __init__(self):
        self._datasource = PollAnswerVoteMemoryDatasource()

    def count_by_answer_id(self, answer_id: str) -> int:
        return len(self._datasource.get_by_answer_id(answer_id))


class PollAnswersManager:
    _updater: PollAnswerStateUpdater
    _reader: PollAnswerStateReader
    _poll_votes: PollAnswerVoteStateReader

    def __init__(self):
        self._updater = PollAnswerStateUpdater()
        self._reader = PollAnswerStateReader()
        self._votes = PollAnswerVoteStateReader()

    def get_by_poll_id(self, poll_id: str) -> List[PollAnswerVotes]:
        result = []
        for answer in self._reader.get_by_poll_id(poll_id):
            votes = self._votes.count_by_answer_id(answer.id)
            result.append(PollAnswerVotes(answer.id, answer.text, votes))

        return result

    def create_bulk(self, poll_id: str, answers: List[PollAnswerSerializer]) -> List[PollAnswerVotes]:
        return [
            PollAnswerVotes(answer.id, answer.poll_id, 0)
            for answer in self._updater.create_bulk(poll_id, answers)
        ]

    def delete_by_product_id(self, poll_id: str) -> None:
        return self._updater.delete_by_poll_id(poll_id)
