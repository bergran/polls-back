from abc import ABCMeta
from typing import List
from uuid import uuid4

from src.modules.polls.data.models import Poll, PollRaw, PollAnswerRaw, PollAnswer, PollAnswerUpdateRaw


class PollAnswerDataSourceBaseException(Exception):
    pass


class PollAnswerRetrieveDataSourceException(PollAnswerDataSourceBaseException):
    pass


class PollAnswerBaseDataSource(metaclass=ABCMeta):
    def get_by_poll_id(self, poll_id: str) -> List[PollAnswer]:
        pass

    def create_bulk(self, polls_raw: List[PollAnswerRaw]) -> List[PollAnswer]:
        pass

    def delete_by_poll_id(self, poll_id: str) -> None:
        pass


class PollAnswerMemoryDataSource(PollAnswerBaseDataSource):
    _polls: List[PollAnswer]
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._polls = list()
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super(PollAnswerMemoryDataSource, self).__init__()

    def get_by_poll_id(self, poll_id: str) -> List[PollAnswer]:
        return [poll_answer for poll_answer in self._polls if poll_answer.poll_id == poll_id]

    def create_bulk(self, polls_raw: List[PollAnswerRaw]) -> List[PollAnswer]:
        to_create = []
        for poll_answer in polls_raw:
            new_poll = PollAnswer(str(uuid4()), poll_answer.text, poll_answer.poll_id)
            to_create.append(new_poll)
            self._polls.append(new_poll)
        return to_create

    def delete_by_poll_id(self, poll_id: str) -> None:
        self._polls = [poll for poll in self._polls if poll.poll_id != poll_id]
