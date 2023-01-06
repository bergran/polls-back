from typing import List

import pytest

from src.modules.polls.data.datasources.poll_answer import PollAnswerMemoryDataSource
from src.modules.polls.data.datasources.poll_question import PollMemoryDataSource
from src.modules.polls.data.models import Poll
from tests.unit.integration.api.polls.fixtures import POLLS, POLL_ANSWERS


@pytest.fixture()
def polls() -> List[Poll]:
    poll_service = PollMemoryDataSource()
    poll_answer_service = PollAnswerMemoryDataSource()
    poll_service._polls = POLLS
    poll_answer_service._polls = POLL_ANSWERS

    yield POLLS
    poll_service._polls = []
    poll_answer_service._polls = []
