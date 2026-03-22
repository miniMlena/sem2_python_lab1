import json
import uuid
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from src.protocols.task import Task
from src.sources.registry import register_source


def parse_json_file(line: str, path: str, line_no: int) -> dict[str, Any]:
    try:
        return json.loads(line)
    except json.JSONDecodeError as error:
        raise ValueError(f"Bad JSON at {path}:{line_no}: {error}") from error


@dataclass(frozen=True)
class JsonlSource:
    path: Path
    name: str = "file-jsonl"

    def fetch(self) -> Iterable[Task]:
        with self.path.open("r", encoding="utf-8") as file:
            for line_no, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                task = parse_json_file(line, str(self.path), line_no)
                task_id = str(task.get("id", f"{self.path.name}:{line_no}"))
                task_title = task.get("title", "")
                task_author = task.get("author", "")
                task_content = task.get("content", "")
                yield Task(
                    id=task_id, title=task_title, author=task_author, message=task_content
                )


@register_source("file-jsonl")
def create_json_source(path: Path) -> JsonlSource:
    return JsonlSource(path=path)