#!/usr/bin/env python3
import re
import sys
from collections import (Counter, deque)
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
        # return [c for c in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)] if self.is_valid(*c)]
        return [c for c in [(x+1,y),(x,y+1)] if self.is_valid(*c)]


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


def flood_fill(grid, current, current_length, path, memo):
    if current in memo and memo[current][0] <= current_length:
        # We already found a shorter path to the current node. No more work
        # to be done
        # print(f'Skipping: {current} {current_length} {memo[current][0]}')
        return

    # print(f'Not skipping: {current} {current_length} {"init" if current not in memo else memo[current][0]}')
    # We never visited this node, or the previous path we found to it is longer
    # than this new one we found
    path = path[:]
    path += [current]

    memo[current] = (current_length, path)

    for neighbor in grid.neighbors(*current):
        flood_fill(grid, neighbor, current_length + grid.get(*neighbor), path, memo)


def part_1(grid):
    memo = dict()
    flood_fill(grid, (0,0), 0, [(0,0)], memo)
    result = memo[(grid.width-1, grid.height-1)]
    print(result)
    grid.print_path(result[1])


def part_2(grid):
    pass


sys.setrecursionlimit(1000000)
grid = read_input()
part_1(grid)
part_2(grid)


