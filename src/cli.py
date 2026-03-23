from pathlib import Path
from typing import Any
import typer
from typer import Typer
from src.base_classes.task_manager import TaskManager
from src.sources.registry import REGISTRY

cli = Typer(no_args_is_help=True)

@cli.command("instruct")
def display_instructions() -> None:
    '''
    Показывает подробную инструкцию по использованию
    '''
    typer.echo("Доступные команды:")
    typer.echo('1) instruct - Выводит это сообщение')
    typer.echo('\tУ этой команды нет опций или аргументов')
    typer.echo('\tПример использования: python -m src instruct')
    typer.echo('')
    typer.echo('2) sources - Выводит список доступных источников задач')
    typer.echo('\tУ этой команды нет опций или аргументов')
    typer.echo('\tПример использования: python -m src sources')
    typer.echo('')
    typer.echo('3) read - Читает и показывает задачи из указанных источников с возможностью фильтрации, имеет несколько опций и аргументов:')
    typer.echo('В качестве аргументов можно указать файлы формата jsonl, тогда задачи будут читаться из них')
    typer.echo('\tПримеры:')
    typer.echo('\tpython -m src read example_1.jsonl')
    typer.echo('\tpython -m src read example_1.jsonl example_2.jsonl')
    typer.echo('--stdin - Считывать задачи из сдандартного ввода')
    typer.echo('\tЗадачи нужно писать в формате id:title:author:content')
    typer.echo('\tЕсли вы захотите перестать вводить задачи, напишите stop')
    typer.echo('\tПример использования:')
    typer.echo('\tpython -m src read --stdin')
    typer.echo('\tДальше вводим задачи, например:   my_id:my_title:my_author:my_content')
    typer.echo('--max_tasks - Установить максимум, сколько задач может быть прочитано')
    typer.echo('\tПо умолчанию 10, если поставить 0, то можно прочитать неограниченное число задач')
    typer.echo('\tПримеры:')
    typer.echo('\tpython -m src read --stdin --max-tasks 5')
    typer.echo('\tpython -m src read example_1.jsonl --max-tasks 0')
    typer.echo('--author - Считывать задачи только указанного автора')
    typer.echo('\tПример:')
    typer.echo('\tpython -m src read --stdin --author milena')
    typer.echo('\tВсе встреченные задачи с другим автором будут проигнорированы и не будут считываться программой')
    typer.echo('--contains - Считывать только задачи с указанной подстрокой в содержании')
    typer.echo('\tПример:')
    typer.echo('\tpython -m src read example_1.jsonl --contains проект')
    typer.echo("\tЗадача '8:Сделать бэкап:milena:Сделать бэкап базы данных проекта' будет считана")
    typer.echo("\tЗадача '9:Написать тесты:cool_user:Написать тесты к лабе по python' не считается")
    typer.echo('Все аргументы и опции можно комбинировать, примеры:')
    typer.echo('python -m src read example_1.jsonl example_2.jsonl --max-tasks 20 --author kate')
    typer.echo('python -m src read example_1.jsonl example_2.jsonl --stdin --max-tasks 20')
    typer.echo('python -m src read example_1.jsonl --stdin --author alina --contains python')
    typer.echo('')

@cli.command("sources")
def list_sources() -> None:
    '''
    Выводит список доступных источников
    '''
    typer.echo("Доступные источники:")
    for name in sorted(REGISTRY):
        typer.echo(name)

def _build_sources(stdin: bool, jsonl: list[Path]) -> list[Any]:
    sources: list[Any] = []
    for path in jsonl:
        sources.append(REGISTRY["jsonl-file"](path))
    if stdin:
        sources.append(REGISTRY["stdin"]())
    return sources

@cli.command("read")
def read(
    stdin: bool = typer.Option(False, "--stdin", help="Прочитать задачи из стандартного ввода (stdin)"),
    jsonl: list[Path] = typer.Argument(
        help="Прочитать задачи из JSONL файлов",
        default_factory=list,
        exists=True,
        dir_okay=False,
        readable=True,
    ),
    max_tasks: int = typer.Option(
        10,
        "--max-tasks",
        help="Максимальное число задач, по умолчанию 10 (0 = без ограничения)",
        min=0,
    ),
    author: str | None = typer.Option(None, "--author", help="Читать задачи только от заданного автора"),
    contains: str | None = typer.Option(None, "--contains", help="Читать только задачи, содержащие заданную подстроку"),
):
    '''
    Читает задачи из указанных источников с возможностью фильтрации по содержанию и автору и показывает считанные задачи
    '''
    raw_sources = _build_sources(stdin, jsonl)
    inbox = TaskManager(raw_sources)
    count = 0
    for tsk in inbox.iter_tasks():
        if author and author != tsk.author:
            continue
        if contains and contains not in tsk.content:
            continue
        count += 1
        typer.echo(f"Считана задача: [{tsk.author}: {tsk.id}] {tsk.title}: {tsk.content}")
        if max_tasks and count >= max_tasks:
            break

    typer.echo(f"\nВсего задач: {count}")
