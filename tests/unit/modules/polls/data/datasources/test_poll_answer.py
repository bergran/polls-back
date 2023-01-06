from typing import List, Optional
from unittest.mock import patch, Mock

from src.modules.polls.data.datasources.poll_answer import (
    PollAnswerMemoryDataSource,
)
from src.modules.polls.data.models import PollAnswer, PollAnswerRaw
from tests.shared.builders import PollAnswerBuilder

POLL_ID_1 = "ba10b7bc-d557-4f37-a471-b8fe2b6200d6"
POLL_ID_2 = "7c7163e0-bd76-4439-ada7-b044f1960361"


POLL_ANSWER = PollAnswerBuilder().with_poll_id(POLL_ID_1).build()
POLL_ANSWER_2 = PollAnswerBuilder().with_poll_id(POLL_ID_1).build()
POLL_ANSWER_3 = PollAnswerBuilder().with_poll_id(POLL_ID_1).build()
POLL_ANSWER_4 = PollAnswerBuilder().with_poll_id(POLL_ID_1).build()
POLL_ANSWER_5 = PollAnswerBuilder().with_poll_id(POLL_ID_2).build()


POLL_ANSWERS = [POLL_ANSWER, POLL_ANSWER_2, POLL_ANSWER_3, POLL_ANSWER_4, POLL_ANSWER_5]
POLL_ANSWERS_POLL_1 = [POLL_ANSWER, POLL_ANSWER_2, POLL_ANSWER_3, POLL_ANSWER_4]


class TestPollAnswerMemory:
    @staticmethod
    def get_service(
        polls: Optional[List[PollAnswer]] = None,
    ) -> PollAnswerMemoryDataSource:
        if polls is None:
            polls = []

        service = PollAnswerMemoryDataSource()
        service._polls = polls
        return service

    def test_list_by_poll_id(self):
        service = self.get_service(POLL_ANSWERS)
        assert service.get_by_poll_id(POLL_ID_1) == POLL_ANSWERS_POLL_1

    @patch("src.modules.polls.data.datasources.poll_answer.uuid4", return_value=POLL_ANSWER.id)
    def test_create_bulk(self, _now_mock: Mock):
        service = self.get_service()
        assert (
            service.create_bulk([PollAnswerRaw(POLL_ANSWER.text, POLL_ANSWER.poll_id)])
            == [POLL_ANSWER]
        )
        assert service._polls == [POLL_ANSWER]

    def test_delete_by_poll_id(self):
        service = self.get_service(POLL_ANSWERS)
        assert service.delete_by_poll_id(POLL_ID_2) is None
        assert service._polls == POLL_ANSWERS_POLL_1
