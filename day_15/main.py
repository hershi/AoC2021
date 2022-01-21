#!/usr/bin/env python3
import re
import sys
from heapq import heappush, heappop
from dataclasses import dataclass, field
from typing import Any
from collections import (Counter, deque)
from itertools import (
    chain,
    repeat,
    zip_longest
)

visit = 0
skip = 0

class Grid:
    def __init__(self, input, multiplier):
        self.width = len(input[0]) * multiplier
        self.height = len(input) * multiplier

        grid = []
        for l in input:
            l = [int(x) for x in l]
            grid.extend(l)
            for i in range(multiplier-1):
                l = [(x % 9 + 1) for x in l]
                grid.extend(l)

        g = grid[:]
        for i in range(multiplier-1):
            g = [(x % 9 + 1) for x in g]
            grid.extend(g)

        self.grid = grid

        print(f'{len(self.grid)} , {self.width}x{self.height} , {self.width * self.height}')


    def get(self, x,y):
        return self.grid[self.width * y + x]


    def is_valid(self,x,y):
        return 0 <= x < self.width and 0 <= y < self.height


    def neighbors(self, x, y):
        return [c for c in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)] if self.is_valid(*c)]
        # return [c for c in [(x+1,y),(x,y+1)] if self.is_valid(*c)]


    def get_path(memo, end):
        current = end
        path = []
        while current:
            path.append(current)
            current = memo[current][1]

        return list(reversed(path))

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

def read_input(multiplier=1):
    with open('./input.txt', 'r') as input_file:
        return Grid([l.strip() for l in input_file.readlines()], multiplier)


@dataclass(order=True)
class ToVisit:
    pos: Any=field(compare=False)
    dist: int
    prev: Any=field(compare=False)

    def __init__(self, pos, dist, prev):
        self.pos = pos
        self.dist = dist
        self.prev = prev

def dijkstra(grid):
    memo = dict()
    to_visit = []

    heappush(to_visit, ToVisit((0,0), 0, None))

    while to_visit:
        current = heappop(to_visit)

        if current.pos in memo and memo[current.pos][0] <= current.dist:
            continue

        memo[current.pos] = (current.dist, current.prev)
        for n in grid.neighbors(*current.pos):
            heappush(to_visit, ToVisit(n, current.dist + grid.get(*n), current.pos))

    return memo

def part_1(grid):
    memo = dijkstra(grid)
    result = memo[(grid.width-1, grid.height-1)]
    print(result)
    grid.print_path(Grid.get_path(memo, result[1]))


sys.setrecursionlimit(1000000)
part_1(read_input(1))
part_1(read_input(5))


