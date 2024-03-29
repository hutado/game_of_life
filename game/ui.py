# -*- coding: utf-8 -*-

"""
Модуль с реализацией графической версии
"""

# built-in
import argparse

from math import floor
from itertools import product

# third-party
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN, KEYDOWN, K_SPACE

# internal
from game_of_life import GameOfLife


# Цвета фона, сетки и живых клеток
POWDER_BLUE = (176, 224, 230)
LIGHT_BLUE = (173, 216, 230)
STEEL_BLUE = (70, 130, 180)


class GUI:
    """
    Класс графического интерфейса
    """

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=10) -> None:
        self.life = life
        self.cell_size = cell_size
        self.speed = speed

        # Настройки окна pygame
        self.width = self.cell_size * life.cols
        self.height = self.cell_size * life.rows
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)

        # Состояния игры
        self.running = True
        self.pause = True

    def draw_lines(self) -> None:
        """
        Отрисовка сетки
        """

        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color(LIGHT_BLUE), (x, 0), (x, self.height))

        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color(LIGHT_BLUE), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """
        Отрисовка клеток с закрашиванием живых
        """

        for c, r in product(range(self.life.curr_generation.cols), range(self.life.curr_generation.rows)):
            color = pygame.Color(STEEL_BLUE) if self.life.curr_generation[r][c] == 1 else pygame.Color(POWDER_BLUE)
            rect = pygame.Rect(c * self.cell_size, r * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, color, rect)

    def draw_elements(self) -> None:
        """
        Отрисовка окна
        """

        self.draw_grid()
        self.draw_lines()

    def check_events(self) -> None:
        """
        Проверка событий нажатия клавиш и состояния игры
        """

        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.pause = True

                    x, y = pygame.mouse.get_pos()

                    x = floor(x / self.cell_size)
                    y = floor(y / self.cell_size)

                    self.life.curr_generation[y][x] = 1 if self.life.curr_generation[y][x] == 0 else 0
                    self.draw_elements()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.pause = not self.pause

    def run(self) -> None:
        """
        Запуск игры
        """

        pygame.init()

        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color(POWDER_BLUE))

        self.draw_elements()

        while self.running:
            self.check_events()

            if not self.pause:
                if self.life.is_changing:
                    self.life.step()
                else:
                    self.pause = True

                self.draw_elements()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Game of Life PyGame',
        description='Графическая версия Conway\'s Game Of Life',
        epilog='Нажмите ПРОБЕЛ, чтобы поставить на паузу или снять с паузы',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument('--rows', required=False, type=int, default=80, help='Количество строк')
    parser.add_argument('--cols', required=False, type=int, default=80, help='Количество столбцов')
    parser.add_argument('--cell-size', required=False, type=int, default=10, help='Размер клетки в px')
    parser.add_argument('-r', '--randomize', required=False, default=False, action='store_true', help='Случайное заполнение поля')
    parser.add_argument('-s', '--speed', required=False, type=int, default=10, help='Скорость игры')
    parser.add_argument('-S', '--survival', required=False, type=str, default='23', help='Необходимое количество соседей для выживания клетки')
    parser.add_argument('-B', '--birth', required=False, type=str, default='3', help='Необходимое количество соседей для рождения клетки')
    parser.add_argument('-i', '--infinity', required=False, default=False, action='store_true', help='Бесконечное поле')

    args = parser.parse_args()

    rows_: int = args.rows
    cols_: int = args.cols
    randomize_: bool = args.randomize
    speed_: int = args.speed
    cell_size_: int = args.cell_size
    s_count: list = [int(i) for i in args.survival]
    b_count: list = [int(i) for i in args.birth]
    infinity_: bool = args.infinity

    game = GameOfLife((rows_, cols_), randomize_, s_count, b_count, infinity_)
    gui = GUI(game, cell_size_, speed_)

    gui.run()
