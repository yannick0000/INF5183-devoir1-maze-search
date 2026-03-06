# astar.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import heapq
import time

from maze import Maze

Coord = Tuple[int, int]

@dataclass
class SearchResult:
    path: List[Coord]
    explored_order: List[Coord]
    explored_count: int
    path_length: int
    elapsed_ms: float


def manhattan(a: Coord, b: Coord) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


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


def astar(maze: Maze) -> SearchResult:
    t0 = time.perf_counter()

    start = maze.start
    goal = maze.goal

    # (f, tie, node)
    pq = []
    tie = 0
    g: Dict[Coord, int] = {start: 0}
    parent: Dict[Coord, Optional[Coord]] = {start: None}

    heapq.heappush(pq, (manhattan(start, goal), tie, start))
    closed = set()
    explored_order: List[Coord] = []

    while pq:
        f, _, node = heapq.heappop(pq)
        if node in closed:
            continue
        closed.add(node)
        explored_order.append(node)

        if node == goal:
            break

        r, c = node
        for nxt in maze.neighbors(r, c):
            tentative = g[node] + 1  # coût réel (chaque pas = 1)
            if nxt in closed:
                continue
            if nxt not in g or tentative < g[nxt]:
                g[nxt] = tentative
                parent[nxt] = node
                tie += 1
                fn = tentative + manhattan(nxt, goal)
                heapq.heappush(pq, (fn, tie, nxt))

    path = reconstruct_path(parent, start, goal)

    t1 = time.perf_counter()
    return SearchResult(
        path=path,
        explored_order=explored_order,
        explored_count=len(explored_order),
        path_length=max(0, len(path) - 1),
        elapsed_ms=(t1 - t0) * 1000.0
    )