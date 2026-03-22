from collections.abc import Iterable
from typing import Protocol, runtime_checkable
from src.protocols.task import Task

@runtime_checkable
class TaskSource(Protocol):
    name: str

    def fetch(self) -> Iterable[Task]:
        ...
