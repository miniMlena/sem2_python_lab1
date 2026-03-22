from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Task:
    id: str
    payload: str
# подумать об атрибутах