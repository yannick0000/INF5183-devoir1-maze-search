# dfs.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import time

from maze import Maze, START, GOAL

Coord = Tuple[int, int]

@dataclass
class SearchResult:
    path: List[Coord]
    explored_order: List[Coord]
    explored_count: int
    path_length: int
    elapsed_ms: float


def reconstruct_path(parent: Dict[Coord, Optional[Coord]], start: Coord, goal: Coord) -> List[Coord]:
    if goal not in parent:
        return []
    cur = goal
    out = []
    while cur is not None:
        out.append(cur)
        cur = parent[cur]
    out.reverse()
    if out and out[0] == start:
        return out
    return []


def dfs(maze: Maze) -> SearchResult:
    t0 = time.perf_counter()

    start = maze.start
    goal = maze.goal

    stack: List[Coord] = [start]
    parent: Dict[Coord, Optional[Coord]] = {start: None}
    visited = {start}

    explored_order: List[Coord] = []

    while stack:
        node = stack.pop()
        explored_order.append(node)

        if node == goal:
            break

        r, c = node
        # Pour respecter l'ordre de visite (droite, bas, gauche, haut),
        # on empile en ordre inverse (pile LIFO).
        neighs = list(maze.neighbors(r, c))
        for nxt in reversed(neighs):
            if nxt not in visited:
                visited.add(nxt)
                parent[nxt] = node
                stack.append(nxt)

    path = reconstruct_path(parent, start, goal)

    t1 = time.perf_counter()
    return SearchResult(
        path=path,
        explored_order=explored_order,
        explored_count=len(explored_order),
        path_length=max(0, len(path) - 1),
        elapsed_ms=(t1 - t0) * 1000.0
    )