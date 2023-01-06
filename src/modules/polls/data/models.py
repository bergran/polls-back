from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Poll:
    id: str
    question: str


@dataclass(frozen=True)
class PollRaw:
    question: str


@dataclass(frozen=True)
class PollAnswer:
    id: str
    text: str
    poll_id: str


@dataclass(frozen=True)
class PollAnswerVotes:
    id: str
    text: str
    votes: int


@dataclass(frozen=True)
class PollAnswerRaw:
    text: str
    poll_id: str


@dataclass(frozen=True)
class PollAnswerUpdateRaw:
    text: str


@dataclass(frozen=True)
class PollResponse:
    id: str
    question_id: str


@dataclass(frozen=True)
class AnswerVote:
    answer_id: str


@dataclass(frozen=True)
class AnswerVoteResponseRaw:
    answer_id: str


@dataclass(frozen=True)
class PollWithAnswers:
    id: str
    question: str
    answers: List[PollAnswerVotes]
