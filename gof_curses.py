# -*- coding: utf-8 -*-

"""
Модуль с реализацией консольной версии
"""

# built-in
import argparse

from itertools import product

# third-party
import curses

# internal
from ui import UI
from game_of_life import GameOfLife


class Console(UI):
    """
    Класс консольного интерфейса
    """

    def __init__(self, speed: int=100) -> None:
        self.screen = self.init_screen()
        self.height, self.width = self.screen.getmaxyx()
        self.life = GameOfLife((self.height - 2, self.width - 2), True)
        self.speed = speed
        self.running = True

        super().__init__(self.life)

    def init_screen(self):
        """
        Настройки окна curses
        """

        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.curs_set(0)
        screen.erase()
        screen.border(0)
        screen.nodelay(True)
        screen.keypad(1)

        return screen

    def draw_grid(self) -> None:
        """
        Отрисовка клеток
        """

        for c, r in product(range(self.life.curr_generation.cols), range(self.life.curr_generation.rows)):
            color = '*' if self.life.curr_generation[r][c] == 1 else ' '
            self.screen.addch(r+1, c+1, color)

    def draw_elements(self) -> None:
        """
        Отрисовка поля
        """

        self.screen.refresh()
        self.draw_grid()
        self.life.step()
        curses.delay_output(self.speed)
        key = self.screen.getch()
        if key in [ord('q'), ord('Q')]:
            self.running = False

    def close_window(self) -> None:
        """
        Финальный экран и закрытие окна
        """

        self.screen.nodelay(False)
        self.screen.erase()
        self.screen.refresh()
        self.screen.getch()
        curses.nocbreak()
        self.screen.keypad(0)
        curses.echo()
        curses.endwin()

    def run(self) -> None:
        """
        Запуск игры
        """

        while self.running and self.life.is_changing:
            self.draw_elements()

        self.close_window()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Game of Life curses',
        description='Консольная версия Conway\'s Game Of Life',
        epilog='Нажмите Q, чтобы выйти из игры',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument('-s', '--speed', required=False, type=int, default=100, help='Задержка обновления')

    args = parser.parse_args()

    speed_: int = args.speed

    gui = Console(speed_)
    gui.run()
