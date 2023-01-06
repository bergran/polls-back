from abc import ABCMeta
from typing import List
from uuid import uuid4

from src.modules.polls.data.models import Poll, PollRaw


class PollDataSourceBaseException(Exception):
    pass


class PollRetrieveDataSourceException(PollDataSourceBaseException):
    pass


class PollBaseDataSource(metaclass=ABCMeta):
    def get(self) -> List[Poll]:
        pass

    def retrieve(self, poll_id: str) -> Poll:
        pass

    def create(self, poll_raw: PollRaw) -> Poll:
        pass

    def update(self, poll_id: str, poll_raw: PollRaw) -> Poll:
        pass

    def delete(self, poll_id: str) -> None:
        pass


class PollMemoryDataSource(PollBaseDataSource):
    _polls: List[Poll]
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._polls = list()
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        super(PollMemoryDataSource, self).__init__()

    def get(self) -> List[Poll]:
        return self._polls

    def retrieve(self, poll_id: str) -> Poll:
        polls = list(filter(lambda poll: poll.id == poll_id, self._polls))

        if len(polls) > 0:
            return polls[0]

        raise PollRetrieveDataSourceException()

    def create(self, poll_raw: PollRaw) -> Poll:
        new_poll = Poll(str(uuid4()), poll_raw.question)
        self._polls.append(new_poll)
        return new_poll

    def update(self, poll_id: str, poll_raw: PollRaw) -> Poll:
        try:
            index = [poll.id for poll in self._polls].index(poll_id)
        except ValueError:
            raise PollRetrieveDataSourceException()

        new_poll = Poll(poll_id, poll_raw.question)
        self._polls[index] = new_poll

        return new_poll

    def delete(self, poll_id: str) -> None:
        self._polls = [poll for poll in self._polls if poll.id != poll_id]
