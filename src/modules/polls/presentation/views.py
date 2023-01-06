from time import sleep
from typing import List

from fastapi import APIRouter, HTTPException

from src.modules.polls.data.datasources.poll_question import (
    PollRetrieveDataSourceException,
)
from src.modules.polls.data.models import Poll
from src.modules.polls.data.serializer import PollSerializer, PollInstanceSerializer, PollAnswerVoteSerializer
from src.modules.polls.domain.poll_user_cases import (
    PollDeleteUserCase,
    PollUpdateUserCase,
    PollRetrieveUserCase,
    PollListUserCase,
    PollCreateUserCase, PollVoteAnswerUserCase,
)

api_router = APIRouter(prefix="/polls")


@api_router.get("/")
def get_polls() -> List[Poll]:
    return PollListUserCase().execute()


@api_router.post("/")
def create_polls(poll_create: PollSerializer) -> PollInstanceSerializer:
    return PollInstanceSerializer.from_orm(PollCreateUserCase().execute(poll_create))


@api_router.get("/{poll_id}/")
def retrieve_polls(poll_id: str) -> PollInstanceSerializer:
    try:
        return PollInstanceSerializer.from_orm(PollRetrieveUserCase().execute(poll_id))
    except PollRetrieveDataSourceException:
        raise HTTPException(status_code=404)


@api_router.put("/{poll_id}/")
def update_polls(poll_id: str, poll_update: PollSerializer) -> Poll:
    try:
        return PollUpdateUserCase().execute(poll_id, poll_update)
    except PollRetrieveDataSourceException:
        raise HTTPException(status_code=404)


@api_router.delete("/{poll_id}/", status_code=204)
def delete_polls(poll_id: str) -> None:
    return PollDeleteUserCase().execute(poll_id)\


@api_router.post("/vote/", status_code=201)
def vote_answer(payload: PollAnswerVoteSerializer) -> None:
    return PollVoteAnswerUserCase().execute(payload)
