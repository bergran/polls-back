from src.modules.polls.data.models import PollWithAnswers
from src.modules.polls.data.serializer import PollSerializer, PollAnswerSerializer
from tests.shared.builders import PollBuilder, PollAnswerBuilder

POLL = PollBuilder().build()
POLL_ANSWER = PollAnswerBuilder().build()
POLLS = [POLL]
POLL_ANSWERS = [POLL_ANSWER]
CREATE_PAYLOAD = PollSerializer(
    question=POLL.question,
    answers=[PollAnswerSerializer(text=POLL_ANSWER.text)],
)
POLL_WITH_ANSWERS = PollWithAnswers(
    id=POLL.id,
    question=POLL.question,
    answers=POLL_ANSWERS
)
