from abc import ABCMeta
from typing import List

from src.modules.polls.data.models import AnswerVote


class PollAnswerVoteBaseDatasource(metaclass=ABCMeta):
    def get_by_answer_id(self, answer_id: str) -> List[AnswerVote]:
        pass


class PollAnswerVoteMemoryDatasource(PollAnswerVoteBaseDatasource):
    _instance = None
    _polls: List[AnswerVote] = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._polls = list()
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def get_by_answer_id(self, answer_id: str) -> List[AnswerVote]:
        return [
            vote_answer
            for vote_answer in self._polls
            if vote_answer.answer_id == answer_id
        ]

    def create_answer_vote(self, answer_vote: AnswerVote) -> AnswerVote:
        self._polls.append(answer_vote)
        return answer_vote
