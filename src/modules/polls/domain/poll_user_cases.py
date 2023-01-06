from abc import ABCMeta
from typing import List

from src.modules.polls.data.datasources.poll_answer import (
    PollAnswerMemoryDataSource,
    PollAnswerBaseDataSource,
)
from src.modules.polls.data.datasources.poll_answer_vote import PollAnswerVoteMemoryDatasource
from src.modules.polls.data.datasources.poll_question import (
    PollBaseDataSource,
    PollMemoryDataSource,
)
from src.modules.polls.data.models import (
    Poll,
    PollRaw,
    PollWithAnswers,
    PollAnswer,
    PollAnswerRaw, AnswerVote,
)
from src.modules.polls.data.serializer import PollSerializer, PollAnswerVoteSerializer
from src.modules.polls.domain.answers_manager import PollAnswersManager


class PollListUserCase(metaclass=ABCMeta):
    _datasource: PollBaseDataSource

    def __init__(self):
        self._datasource = PollMemoryDataSource()

    def execute(self) -> List[Poll]:
        return self._datasource.get()


class PollCreateUserCase(metaclass=ABCMeta):
    _poll_datasource: PollBaseDataSource
    _poll_answer_datasource: PollAnswerBaseDataSource

    def __init__(self):
        self._poll_datasource = PollMemoryDataSource()
        self._poll_answer_manager = PollAnswersManager()

    def execute(self, create_poll: PollSerializer) -> PollWithAnswers:
        poll = self._poll_datasource.create(PollRaw(create_poll.question))

        poll_answers = self._poll_answer_manager.create_bulk(poll.id, create_poll.answers)
        return PollWithAnswers(poll.id, poll.question, poll_answers)


class PollRetrieveUserCase(metaclass=ABCMeta):
    _poll_datasource: PollBaseDataSource
    _poll_answer_manager: PollAnswersManager

    def __init__(self):
        self._poll_datasource = PollMemoryDataSource()
        self._poll_answer_manager = PollAnswersManager()

    def execute(self, poll_id: str) -> PollWithAnswers:
        poll = self._poll_datasource.retrieve(poll_id)
        answers = self._poll_answer_manager.get_by_poll_id(poll_id)
        return PollWithAnswers(poll.id, poll.question, answers)


class PollUpdateUserCase(metaclass=ABCMeta):
    _datasource: PollBaseDataSource

    def __init__(self):
        self._datasource = PollMemoryDataSource()

    def execute(self, poll_id: str, poll_update: PollSerializer) -> Poll:
        return self._datasource.update(poll_id, PollRaw(poll_update.question))


class PollDeleteUserCase(metaclass=ABCMeta):
    _poll_datasource: PollBaseDataSource
    _poll_answer_datasource: PollAnswerBaseDataSource

    def __init__(self):
        self._poll_datasource = PollMemoryDataSource()
        self._poll_answer_datasource = PollAnswerMemoryDataSource()

    def execute(self, poll_id: str) -> None:
        self._poll_datasource.delete(poll_id)
        self._poll_answer_datasource.delete_by_poll_id(poll_id)


class PollVoteAnswerUserCase(metaclass=ABCMeta):
    _poll_answer_vote: PollAnswerVoteMemoryDatasource

    def __init__(self):
        self._poll_answer_datasource = PollAnswerVoteMemoryDatasource()

    def execute(self, answer_vote: PollAnswerVoteSerializer) -> None:
        self._poll_answer_datasource.create_answer_vote(AnswerVote(answer_vote.answer_id))
