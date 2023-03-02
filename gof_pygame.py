# -*- coding: utf-8 -*-

"""
Модуль с реализацией графической версии
"""

import argparse

import pygame
from pygame.locals import *

from math import floor
from itertools import product

from ui import UI
from game_of_life import GameOfLife


class GUI(UI):
    """
    Класс графического интерфейса
    """

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=10) -> None:
        self.life = life
        self.cell_size = cell_size
        self.speed = speed

        super().__init__(life)

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
            pygame.draw.line(self.screen, pygame.Color('black'), (x, 0), (x, self.height))

        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        """
        Отрисовка клеток с закрашиванием живых
        """

        for c, r in product(range(self.life.curr_generation.cols), range(self.life.curr_generation.rows)):
            color = pygame.Color('green') if self.life.curr_generation[r][c] == 1 else pygame.Color('white')
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
        self.screen.fill(pygame.Color('white'))

        self.draw_elements()

        while self.running:
            self.check_events()

            if not self.pause:
                if self.life.is_changing and not self.life.is_max_generations_exceeded:
                    self.life.step()
                else:
                    self.pause = True

                self.draw_elements()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()
        print(f'Количество поколений: {self.life.generations}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Game of Life PyGame',
        description='Графическая версия Conway\'s Game Of Life',
        epilog='Нажмите ПРОБЕЛ, чтобы поставить на паузу или снять с паузы',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument('--height', required=False, type=int, default=300, help='Высота окна в px')
    parser.add_argument('--width', required=False, type=int, default=500, help='Ширина окна в px')
    parser.add_argument('--cell-size', required=False, type=int, default=20, help='Размер клетки в px')
    parser.add_argument('-r', '--randomize', required=False, default=False, action='store_true', help='Случайное заполнение поля')
    parser.add_argument('-s', '--speed', required=False, type=int, default=10, help='Скорость игры')

    args = parser.parse_args()

    height_ = args.height
    width_ = args.width
    cell_size_ = args.cell_size
    randomize_ = args.randomize
    speed_ = args.speed

    game = GameOfLife((height_ // cell_size_, width_ // cell_size_), randomize_)
    gui = GUI(game, cell_size_, speed_)

    gui.run()
