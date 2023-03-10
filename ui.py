# -*- coding: utf-8 -*-

"""
Модуль с базовым классом интерфейса
"""

import abc

from game_of_life import GameOfLife


class UI(abc.ABC):

    def __init__(self, life: GameOfLife) -> None:
        self.life = life

    @abc.abstractmethod
    def run(self) -> None:
        pass
