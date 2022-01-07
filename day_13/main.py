#!/usr/bin/env python3
import re
from itertools import (
    chain,
    repeat,
)

def read_input():
    with open('./input.txt', 'r') as input_file:
        lines = input_file.readlines()

    points = [l.strip().split(',') for l in lines if re.match('\d+,\d+', l)]
    points = set([(int(x), int(y)) for x,y in points])
    folds = [re.match('.*(.)=(\d+)', l).groups() for l in lines if re.match('fold.*', l)]
    folds = [(axis, int(num)) for axis,num in folds]
    return points,folds

def horizontal_fold(point, num):
    if point[1] < num:
        return point

    diff = point[1] - num
    return (point[0], point[1] - (2*diff))

def vertical_fold(point, num):
    if point[0] < num:
        return point

    diff = point[0] - num
    new_point = point[0] - (2*diff), point[1]
    return new_point


def fold(points, fold):
    axis,num = fold
    if axis == 'x':
        return set([vertical_fold(point, num) for point in points])

    if axis == 'y':
        return set([horizontal_fold(point, num) for point in points])


def print_points(points):
    width = max([p[0] for p in points])
    height = max([p[1] for p in points])
    for y in range(height+1):
        print('')
        for x in range(width+1):
            print('#' if (x,y) in points else ' ', end='')



def part_1(points, folds):
    folded = fold(points, folds[0])
    print(f'Part 1: {len(folded)}')


def part_2(points, folds):
    for f in folds:
        points = fold(points, f)

    print(f'Part 2: {len(points)}')
    print_points(points)


points,folds = input = read_input()
part_1(points.copy(), folds)
part_2(points.copy(), folds)


