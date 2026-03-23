import pytest
from unittest.mock import Mock
import io
from pathlib import Path
from dataclasses import dataclass
from dataclasses import FrozenInstanceError
from src.base_classes.task import Task
from src.base_classes.task_source import TaskSource
from src.base_classes.task_manager import TaskManager
from src.sources.json import JsonlSource
from src.sources.stdin import StdinLineSource, extract_tasks
from src.sources.registry import REGISTRY

task_example = Task(id='fake_id', title='fake_title', author='fake_author', content='fake_content')

@dataclass(frozen=True)
class FakeTask:
    id: str = "fake"
    title: str = "Fake"
    author: str = "Fake Author"
    content: str = "Fake content"

class FakeTaskSource:
    name = 'fake_name'

    def get_tasks(self):
        yield FakeTask()

class NotSource:
    pass

def test_isinstance_protocol():
    '''
    Тестируем, что протокол TaskSource корректно работает с isinstance()
    и источником, исполняющим протокол 
    '''
    source = FakeTaskSource()
    assert isinstance(source, TaskSource)

def test_isinstance_not_protocol():
    '''
    Тестируем, что протокол TaskSource корректно работает с isinstance()
    и источником, не исполняющим протокол 
    '''
    source = NotSource()
    assert not isinstance(source, TaskSource)

def test_task_frozen():
    '''Тест, что задачу нельзя изменить после создания'''
    task = Task(id="1", title="test", author="author", content="content")
    with pytest.raises(FrozenInstanceError):
        task.title = "New"

def test_json_source_invalid_json():
    '''Тест с невалидным JSON файлом'''
    path = Path("invalid.jsonl")
    path.write_text('{"id": "1" invalid}')
    source = JsonlSource(path=path, name="test")
    with pytest.raises(ValueError):
        next(source.get_tasks())

def test_stdin_source_valid_data():
    '''Тест StdinLineSource с валидными данными'''
    fake_stdin = io.StringIO("id1:title1:author1:content1\nid2:title2:author2:content2\nstop\n")
    source = StdinLineSource(stream=fake_stdin, name="test")
    
    tasks = list(source.get_tasks())
    assert len(tasks) == 2
    assert tasks[0].id == "id1"
    assert tasks[0].title == "title1"
    assert tasks[1].author == "author2"

def test_stdin_source_invalid_line_raises():
    '''Тестируем некорректную строку с StdinLineSource'''
    fake_stdin = io.StringIO("too:few:fields\nstop\n")
    source = StdinLineSource(stream=fake_stdin, name="test")
    
    with pytest.raises(ValueError, match="Некорректная строка: 1"):
        list(source.get_tasks())

def test_stdin_source_empty_skip():
    """Тест, что StdinLineSource пропускает пустые строки"""
    fake_stdin = io.StringIO("\n\nid:title:author:content\nstop\n")
    source = StdinLineSource(stream=fake_stdin, name="test")
    
    tasks = list(source.get_tasks())
    assert len(tasks) == 1

def test_stdin_source_no_stop_reads_all():
    """Тест, что без указания stop_sign задачи считываются до конца"""
    fake_stdin = io.StringIO("id:title:author:content\nid2:title2:author2:content2\n")
    source = StdinLineSource(stream=fake_stdin, name="test")
    
    tasks = list(source.get_tasks())
    assert len(tasks) == 2

def test_extract_tasks_function():
    """Тестируем extract_tasks"""
    lines = ["id", "title", "author", "content"]
    result = extract_tasks(lines, line_no=1)
    assert result == ("id", "title", "author", "content")

def test_taskmanager_iter_empty():
    '''Тест пустого менеджера задач'''
    manager = TaskManager()
    assert list(manager.iter_tasks()) == []

def test_taskmanager_single_source():
    '''Тестируем менеджер задач с 1 источником'''
    source = FakeTaskSource()
    manager = TaskManager(sources=[source])
    tasks = list(manager.iter_tasks())
    assert len(tasks) == 1
    assert tasks[0].title == "Fake"

def test_taskmanager_invalid_source():
    '''Тест менеджера задач с некорректным источником'''
    manager = TaskManager(sources=[NotSource()])
    with pytest.raises(TypeError):
        list(manager.iter_tasks())

def test_taskmanager_multiple_sources():
    '''Тест менеджера задач с несколькими источниками'''
    source1 = FakeTaskSource()
    source2 = Mock(spec=TaskSource)
    source2.get_tasks.return_value = [FakeTask(id="2")]
    manager = TaskManager(sources=[source1, source2])
    tasks = list(manager.iter_tasks())
    assert len(tasks) == 2

def test_registry_json_registered():
    '''Тест, что json файлы есть среди доступных источников'''
    assert "jsonl-file" in REGISTRY

def test_registry_stdin_registered():
    '''Тестируем, что stdin есть среди доступных источников'''
    assert "stdin" in REGISTRY

def test_registry_create_json():
    '''Тест, что введенный json файл проходит регистрацию'''
    path = Path("test.jsonl")
    source = REGISTRY["jsonl-file"](path)
    assert isinstance(source, JsonlSource)