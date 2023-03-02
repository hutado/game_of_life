# -*- coding: utf-8 -*-

"""
Модуль с реализацией консольной версии
"""

import curses

from ui import UI
from game_of_life import GameOfLife


class Console(UI):
    """
    Класс консольного интерфейса
    """

    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку """
        pass

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток """
        pass

    def run(self) -> None:
        screen = curses.initscr()
        # PUT YOUR CODE HERE
        curses.endwin()
