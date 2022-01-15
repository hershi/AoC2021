#!/usr/bin/env python3
import re
import sys
from collections import Counter
from itertools import (
    chain,
    repeat,
    zip_longest
)

class Grid:
    def __init__(self, input):
        self.width = len(input[0])
        self.height = len(input)
        self.grid = [int(x) for x in chain(*input)]


    def get(self, x,y):
        return self.grid[self.width * y + x]


    def is_valid(self,x,y):
        return 0 <= x < self.width and 0 <= y < self.height


    def neighbors(self, x, y):
        return [c for c in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)] if self.is_valid(*c)]


    def print_path(self, path):
        grid = self.grid[:]
        for x,y in [(x,y) for x in range(self.width) for y in range(self.height)]:
            if (x,y) not in path:
                grid[y*self.height + x] = '.'

        for y in range(self.height):
            s=''
            for x in range(self.width):
                s+=f'{grid[y * self.height + x]}'
            print(s)

def read_input():
    with open('./input.txt', 'r') as input_file:
        return Grid([l.strip() for l in input_file.readlines()])


def _dfs(grid, current, end_node, visited, memo):
    # End of route? Count it as 1
    if current == end_node:
        return grid.get(*current), [end_node]

    # Invalid move (already visited)
    if current in visited:
        return None


    if current in memo:
        return memo[current]

    # Neither of the above?
    # Mark this cave as visited
    # Count the number of paths that continue through each neighbor and add them up
    visited = visited.copy()
    visited.add(current)

    # print(f'{len(visited)} {current}: {memo}')
    paths = [_dfs(grid, n, end_node, visited, memo) for n in grid.neighbors(*current)]
    paths = [p for p in paths if p]

    if not paths:
        return None

    p = min(paths, key=lambda x:x[0])
    memo[current] = (p[0] + grid.get(*current), p[1] + [current])
    return memo[current]


def dfs(grid):
    return _dfs(grid, (0,0), (grid.width-1, grid.height-1), set(), dict())

def part_1(grid):
    result = dfs(grid)
    print(result)
    print()
    grid.print_path(result[1])


def part_2(grid):
    pass


sys.setrecursionlimit(1000000)
grid = read_input()
part_1(grid)
part_2(grid)


