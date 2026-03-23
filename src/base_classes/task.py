from dataclasses import dataclass

# frozen -ельзя изменить задачу после создания, slots - нельзя создавать другие поля, кроме указанных
@dataclass(frozen=True , slots=True)
class Task:
    '''
    Класс для задач
    '''
    id: str
    title: str
    author: str
    content: str