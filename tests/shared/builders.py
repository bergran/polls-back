from abc import ABCMeta
from copy import deepcopy
from functools import partial
from typing import TypeVar, Generic, Dict, Any, List

from src.modules.polls.data.models import Poll, PollAnswer

Model = TypeVar("Model")


class BaseBuilder(Generic[Model], metaclass=ABCMeta):
    model: Model
    default_values: Dict[str, Any]
    _extra_values: Dict[str, Any]

    def __init__(self):
        self._extra_values = dict()

        self._check_default_fields()

    def __getattr__(self, item: str) -> Any:
        if item.startswith("with_"):
            field = item[5:]

            if field in self._get_model_fields():
                return partial(self._add_to_extra_values, field=field)
            raise ValueError(f"Field {field} does not exists on {Model}")
        return super(BaseBuilder, self).__getattribute__(item)

    def _get_model_fields(self) -> List[str]:
        return self.model.__dataclass_fields__

    def _add_to_extra_values(self, value: Any, field: str) -> "BaseBuilder":
        self._extra_values[field] = value
        return self

    def _check_default_fields(self):
        fields = self._get_model_fields()

        for field in self.default_values:
            if field not in fields:
                raise ValueError(f"Field {field} does not exists")

    def build(self) -> Model:
        data = deepcopy(self.default_values)
        data.update(deepcopy(self._extra_values))
        print(f"{self}, {self.default_values} {self._extra_values}")
        return self.model(**data)


POLL_ID = "992828ed-fb84-45be-aebd-48d5d35b9477"


class PollBuilder(BaseBuilder[Poll]):
    model = Poll
    default_values = {
        "id": "992828ed-fb84-45be-aebd-48d5d35b9477",
        "question": "pepe"
    }


POLL_ANSWER_ID = "54639c96-a411-4b19-82aa-81841938ec10"


class PollAnswerBuilder(BaseBuilder[PollAnswer]):
    model = PollAnswer
    default_values = {
        "id": POLL_ANSWER_ID,
        "text": "pepe",
        "poll_id": POLL_ID
    }
