# main.py
#execution algorithme de recherche 
#TAGOU NZOGANG YANNICK MARSSINE
from __future__ import annotations
from typing import List, Tuple

from maze import generate_maze, render_grid, WALL, FREE, START, GOAL, Maze

from dfs import dfs
from bfs import bfs
from astar import astar

Coord = Tuple[int, int]


def mark_exploration(maze: Maze, explored: List[Coord]) -> List[List[str]]:
    g = maze.copy_grid()
    for (r, c) in explored:
        if g[r][c] in (START, GOAL, WALL):
            continue
        g[r][c] = 'p'
    return g


def mark_solution(maze: Maze, path: List[Coord]) -> List[List[str]]:
    g = maze.copy_grid()
    for (r, c) in path:
        if g[r][c] in (START, GOAL, WALL):
            continue
        g[r][c] = '*'
    return g


def format_path(path: List[Coord], start: Coord, goal: Coord) -> str:
    if not path:
        return "Aucun chemin trouvé."
    # Ex: S(1,1) -> (2,1) -> ... -> G(14,14)
    chunks = []
    for i, (r, c) in enumerate(path):
        if i == 0:
            chunks.append(f"S({r},{c})")
        elif i == len(path) - 1:
            chunks.append(f"G({r},{c})")
        else:
            chunks.append(f"({r},{c})")
    return " -> ".join(chunks)


def run_one(name: str, maze: Maze, solver_fn):
    print("\n" + "+" * 40)
    print(f"{name}")
    print("+" * 35)

    result = solver_fn(maze)

    # Exploration
    exp_grid = mark_exploration(maze, result.explored_order)
    print("\n[Exploration] (p = represente les cases explorées)")
    print(render_grid(exp_grid))

    # Solution
    sol_grid = mark_solution(maze, result.path)
    print("\n[Solution] (* = chemin explorer)")
    print(render_grid(sol_grid))

    # Chemin
    print("\n[Chemin explorer]")
    print(format_path(result.path, maze.start, maze.goal))

    # Statistiques
    print("\n[Statistiques]")
    print(f"- Nœuds explorés : {result.explored_count}")
    print(f"- Longueur chemin : {result.path_length}")
    print(f"- Temps (ms) : {result.elapsed_ms:.3f}")

    return result


def main():
    
    seed = 42
    maze = generate_maze(size=16, seed=seed, open_density=0.30)

    print("Labyrinthe généré (seed =", seed, ")")
    print(render_grid(maze.grid))

    r_dfs = run_one("DFS", maze, dfs)
    r_bfs = run_one("BFS", maze, bfs)
    r_ast = run_one("A* (Manhattan)", maze, astar)

    # Tableau comparatif
    print("\n" + "=" * 70)
    print("Tableau comparatif")
    #print("=" * 70)
    print(f"{'Algorithme':<15} {'Noeuds':>8} {'Longueur':>10} {'Temps (ms)':>12}")
   # print("-" * 50)
    print(f"{'DFS':<15} {r_dfs.explored_count:>8} {r_dfs.path_length:>10} {r_dfs.elapsed_ms:>12.3f}")
    print(f"{'BFS':<15} {r_bfs.explored_count:>8} {r_bfs.path_length:>10} {r_bfs.elapsed_ms:>12.3f}")
    print(f"{'A* (manhattan)':<15} {r_ast.explored_count:>8} {r_ast.path_length:>10} {r_ast.elapsed_ms:>12.3f}")


if __name__ == "__main__":
    main()