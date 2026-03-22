import sys
from collections.abc import Iterable
from dataclasses import dataclass
from typing import TextIO

from src.protocols.task import Task
from src.sources.registry import register_source

def extract_messages(lines: list[str], line_no: int) -> tuple[str, str, str, str]:
    try:
        return lines[0], lines[1], lines[2], lines[3]
    except IndexError:
        raise ValueError(
            f"Line: {line_no}. Message must contain at least 4 items, separated by ':' "
        )

@dataclass(frozen=True)
class StdinLineSource:
    stream: TextIO = sys.stdin
    name: str = "stdin"

    def fetch(self) -> Iterable[Task]:
        for line_no, line in enumerate(self.stream, start=1):
            lines = line.split(":")
            if not line.strip():
                continue
            id, title, author, content = extract_messages(lines, line_no)
            yield Task(id=id, title=title, author=author, message=content)

@register_source("stdin")
def create_source() -> StdinLineSource:
    return StdinLineSource()