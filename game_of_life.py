# -*- coding: utf-8 -*-

"""
Модуль с базовыми классами игры
"""

from __future__ import annotations

from copy import deepcopy
from random import choice
from itertools import product


class Grid:
    """
    Класс сетки
    """

    def __init__(self, grid: list[list[int]]) -> None:
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0])

    def __getitem__(self, key: int) -> list:
        return self.grid[key]

    def __eq__(self, other_grid: Grid) -> bool:
        return self.grid.__eq__(other_grid.grid)

    def __repr__(self) -> str:
        return repr(self.grid)


class Cell:
    """
    Класс клетки
    """

    def __init__(self, row: int, col: int) -> None:
        self.row, self.col = row, col


class GameOfLife:
    """
    Conway's Game Of Life
    Игра "Жизнь"
    """

    def __init__(self, size: tuple[int, int], randomize: bool=True, max_generations: int=None) -> None:
        # Размер поля
        self.rows, self.cols = size
        # Предыдущее поколение
        self.prev_generation = self.create_grid()
        # Текущее поколение
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное количество поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool=False) -> Grid:
        """
        Создание списка клеток
        Клетка живая, если значение 1, иначе мертвая, значение 0

        Parameters
        ----------
        randomize : bool
            Если True, то заполняется случайно, иначе все клетки мертвые

        Returns
        -------
        out : Grid
            Заполненная сетка
        """

        return Grid([[choice([0, 1]) if randomize else 0 for _ in range(self.cols)] for _ in range(self.rows)])

    def count_neighbours(self, cell: Cell) -> int:
        """
        Подсчет количества соседних клеток

        Parameters
        ----------
        cell : Cell
            Клетка с координатами

        Returns
        -------
        out : int
            Количество соседей
        """

        neighbours = 0

        for r, c in product(range(-1, 2), range(-1, 2)):
            row_ = r + cell.row
            column_ = c + cell.col

            if 0 <= row_ < self.curr_generation.rows and 0 <= column_ < self.curr_generation.cols:
                neighbours += self.curr_generation[row_][column_]

        return neighbours - self.curr_generation[cell.row][cell.col]

    def get_next_generation(self) -> Grid:
        """
        Получение следующего поколения

        Returns
        -------
        out : Grid
            Новое поколение
        """

        new_generation = deepcopy(self.curr_generation)

        for row, col in product(range(self.curr_generation.rows), range(self.curr_generation.cols)):
            neighbours = self.count_neighbours(Cell(row, col))

            if self.curr_generation[row][col] == 1 and (neighbours < 2 or neighbours > 3):
                new_generation[row][col] = 0
            elif self.curr_generation[row][col] == 0 and neighbours == 3:
                new_generation[row][col] = 1

        return new_generation

    def step(self) -> None:
        """
        Один шаг игры
        """

        new_generation = self.get_next_generation()
        self.prev_generation, self.curr_generation = self.curr_generation, new_generation

        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Признак превышения максимального числа поколений
        """

        return self.max_generations is not None and self.generations > self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Признак изменения состояния с предыдущего
        """

        return self.prev_generation != self.curr_generation

    def __repr__(self) -> str:
        return repr(self.curr_generation)
