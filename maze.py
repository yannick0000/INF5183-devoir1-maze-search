# maze.py
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Optional, Iterable
import random

Coord = Tuple[int, int]  # (row, col)

WALL = '#'
FREE = '.'
START = 'S'
GOAL = 'G'

# Ordre demandé (droite, bas, gauche, haut)
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


@dataclass
class Maze:
    grid: List[List[str]]
    start: Coord
    goal: Coord

    @property
    def n(self) -> int:
        return len(self.grid)

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.n and 0 <= c < self.n

    def is_wall(self, r: int, c: int) -> bool:
        return self.grid[r][c] == WALL

    def neighbors(self, r: int, c: int) -> Iterable[Coord]:
        for dr, dc in DIRS:
            rr, cc = r + dr, c + dc
            if self.in_bounds(rr, cc) and not self.is_wall(rr, cc):
                yield (rr, cc)

    def copy_grid(self) -> List[List[str]]:
        return [row[:] for row in self.grid]


def generate_maze(size: int = 16, seed: Optional[int] = None, open_density: float = 0.30) -> Maze:
    """
    - Bords = murs
    - S en (1,1)
    - G en (size-2, size-2)
    - Chemin garanti S -> G
    """
    if size < 6:
        raise ValueError("size should be >= 6 for meaningful maze.")

    rng = random.Random(seed)

    # 1) Tout en murs
    grid = [[WALL for _ in range(size)] for _ in range(size)]

    start = (1, 1)
    goal = (size - 2, size - 2)

    # 2) Creuser un chemin garanti de S vers G
    r, c = start
    grid[r][c] = FREE

    # On avance jusqu'à atteindre goal (random walk biaisé vers goal)
    while (r, c) != goal:
        moves = []
        # Prioriser les mouvements qui rapprochent de G, mais garder du hasard
        if c < goal[1]:
            moves.append((0, 1))
        if r < goal[0]:
            moves.append((1, 0))
        if c > goal[1]:
            moves.append((0, -1))
        if r > goal[0]:
            moves.append((-1, 0))

        # On ajoute aussi des mouvements latéraux possibles pour varier le chemin
        moves += DIRS

        dr, dc = rng.choice(moves)
        rr, cc = r + dr, c + dc

        # rester à l'intérieur (sans toucher le bord)
        if 1 <= rr <= size - 2 and 1 <= cc <= size - 2:
            r, c = rr, cc
            grid[r][c] = FREE

    # 3) Ouvrir d'autres cases aléatoires (bruit), bords restent murs
    for i in range(1, size - 1):
        for j in range(1, size - 1):
            if (i, j) in (start, goal):
                continue
            if grid[i][j] == WALL and rng.random() < open_density:
                grid[i][j] = FREE

    # 4) Placer S et G
    grid[start[0]][start[1]] = START
    grid[goal[0]][goal[1]] = GOAL

    return Maze(grid=grid, start=start, goal=goal)


def render_grid(grid: List[List[str]]) -> str:
    return "\n".join(" ".join(row) for row in grid)