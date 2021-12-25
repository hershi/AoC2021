#!/usr/bin/env python3

from itertools import chain
from collections import Counter
from numpy import prod


class Grid:
    def __init__(self, values, width):
        self.values = values
        self.width = width
        self.height = len(values) // width

    def get(self, x,y):
        return self.values[x + y*self.width]


    def is_low_point(self, x, y):
        p = self.get(x,y)
        return all(map(lambda m: self.get(*m) > p, self.neighbors(x,y)))

    def neighbors(self, x,y):
        return list(filter(lambda c: self._valid_coordinates(*c),
               [
                   (x+1, y),
                   (x-1, y),
                   (x, y+1),
                   (x, y-1),
               ]
        ))


    def _valid_coordinates(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height


    def __repr__(self):
        res = ""
        for l in zip(*[iter(self.values)]*self.width):
            res += "".join(str(d) for d in l) + "\n"

        return res


    class Iterator:
        def __init__(self, values):
            self.values = values
            self.i = 0


        def __next__(self):
            if self.i >= len(self.values):
                raise StopIteration

            self.i += 1
            return self.values[self.i - 1]

    def __iter__(self):
        return Grid.Iterator(self.values)



def read_input():
    with open('./input.txt', 'r') as input_file:
        lines = input_file.readlines()
        width = len(lines[0].strip())
        values = [int(d) for line in lines for d in line.strip()]
        return Grid(values, width)


def get_low_points(input):
    return [(x, y) for x in range(input.width) for y in range(input.height) if input.is_low_point(x,y)]


def part_1(input):
    s = 0
    s = sum([input.get(*p)+1 for p in get_low_points(input)])

    print(f'Part 1: {s}')


def get_basin(input, p):
    to_visit = [p]

    basin = set()
    while to_visit:
        # print(f'To visit({p}): {to_visit}')
        p = to_visit.pop()
        p_val = input.get(*p)

        if p_val >= 9:
            continue

        basin.add(p)
        to_visit.extend([c for c in input.neighbors(*p) if input.get(*c) > p_val])

    return basin


def part_2(input):
    basins = [get_basin(input, p) for p in get_low_points(input)]
    s = prod([len(basin) for basin in sorted(basins, key=len, reverse=True)[:3]])
    print(f'Product of the sizes of 3 biggest basins is: {s}')


input = read_input()
part_1(input)
part_2(input)


