# -*- coding: utf-8 -*-

"""
Модуль с базовым классом интерфейса
"""

# built-in
import abc

# internal
from game_of_life import GameOfLife


class UI(abc.ABC):

    def __init__(self, life: GameOfLife) -> None:
        self.life = life

    @abc.abstractmethod
    def run(self) -> None:
        pass
