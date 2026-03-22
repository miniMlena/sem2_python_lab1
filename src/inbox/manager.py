from collections.abc import Sequence, Iterable
from src.protocols.task import Task
from src.protocols.task_source import TaskSource

class TaskManager:
    def __init__(self, sources: Sequence[TaskSource] = None):
        self._sources = sources or []

    def iter_tasks(self) -> Iterable[Task]:
        for source in self._sources:
            if not isinstance(source, TaskSource):
                raise TypeError("Источник должен соответствовать протоколу TaskSource")
            for task in source.fetch():
                yield task
