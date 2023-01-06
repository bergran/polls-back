from dataclasses import asdict
from unittest.mock import ANY

from src.modules.polls.data.models import Poll, PollWithAnswers
from src.modules.polls.data.serializer import PollInstanceSerializer
from tests.shared.builders import PollAnswerBuilder

POLL = Poll("7a8a2b22-1f1c-41fa-a8f4-5384eb0066d8", "Test")
POLL_2 = Poll("a6d73811-ded6-44a8-94a7-d3a381fcd5a5", "Test2")
POLL_3 = Poll("8698abab-9ed5-4070-87ad-a74ba11cf0cb", "Test3")
POLLS = [POLL, POLL_2, POLL_3]

POLL_ANSWER = PollAnswerBuilder().with_poll_id(POLL.id).build()
POLL_ANSWERS = [POLL_ANSWER]

RESPONSE_RETRIEVE_POLL = PollInstanceSerializer.from_orm(PollWithAnswers(POLL.id, POLL.question, [POLL_ANSWER]))
QUESTION_UPDATED = "updated"
PAYLOAD_REQUEST_UPDATED_POLL = {"question": QUESTION_UPDATED, "answers": [{"text": POLL_ANSWER.text}]}
PAYLOAD_CREATED_POLL = {"id": ANY, "question": QUESTION_UPDATED, "answers": [{"id": ANY, "text": POLL_ANSWER.text}]}
PAYLOAD_UPDATED_POLL = {"id": POLL.id, "question": QUESTION_UPDATED}

RESPONSE_POLLS = [
    asdict(POLL),
    asdict(POLL_2),
    asdict(POLL_3),
]
