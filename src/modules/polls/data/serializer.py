from typing import List

from pydantic import BaseModel, Field


class PollAnswerSerializer(BaseModel):
    text: str


class PollAnswerInstanceSerializer(BaseModel):
    id: str
    text: str
    votes: int

    class Config:
        orm_mode = True


class PollSerializer(BaseModel):
    question: str
    answers: List[PollAnswerSerializer] = Field(default=list)


class PollInstanceSerializer(BaseModel):
    id: str
    question: str
    answers: List[PollAnswerInstanceSerializer] = Field(default=list)

    class Config:
        orm_mode = True


class PollAnswerVoteSerializer(BaseModel):
    answer_id: str
