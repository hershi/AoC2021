#!/usr/bin/env python3

from enum import Enum
from itertools import chain

class Point:
    def __init__(self, text):
        self.x, self.y = [int(n) for n in text.split(",")]


class Line:
    def __init__(self, text):
        self.p1, self.p2 = [Point(p) for p in text.strip().split(" -> ")]

        if self.p1.x == self.p2.x or self.p1.y == self.p2.y:
            self.is_straight = True
        else:
            self.is_straight = False


    def points(self):
        if self.p1.x == self.p2.x:
            low, high = sorted([self.p1.y, self.p2.y])
            return [(self.p1.x, y) for y in range(low, high+1)]
        elif self.p1.y == self.p2.y:
            low, high = sorted([self.p1.x, self.p2.x])
            return [(x, self.p1.y) for x in range(low, high+1)]
        else:
            # Diagonal line: Order points based on X cooridnates, so we produce
            # points in ascending X values.
            # Now check if Y values should also be ascending or descending, and
            # calculate based on that
            p1, p2 = (self.p1, self.p2) if self.p1.x < self.p2.x else (self.p2, self.p1)
            y_step = 1 if p1.y < p2.y else -1

            return list(zip(range(p1.x, p2.x+1), range(p1.y, p2.y + y_step, y_step)))


def read_input():
    with open('./input.txt', 'r') as input_file:
        return [Line(l) for l in input_file.readlines()]


def part_1(input):
    points = {}

    for p in chain.from_iterable([l.points() for l in input if l.is_straight]):
        points[p] = points.get(p, 0) + 1

    print(len(list(filter(lambda e: e[1] > 1, points.items()))))


def part_2(input):
    points = {}

    for p in chain.from_iterable([l.points() for l in input]):
        points[p] = points.get(p, 0) + 1

    print(len(list(filter(lambda e: e[1] > 1, points.items()))))

input = read_input()
part_1(input)
part_2(input)


