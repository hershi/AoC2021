#!/usr/bin/env python3
from itertools import (
    chain,
    repeat,
)

def process_line(line):
    a,b = line.strip().split('-')
    return [(a,b),(b,a)]

def read_input():
    with open('./input.txt', 'r') as input_file:
        pairs = chain(*[process_line(line) for line in input_file.readlines()])
        res = {}
        for k,v in pairs:
            res.setdefault(k, set([]))
            res[k].add(v)

        return res


def get_limit(node, special_used):
    if node in ['start', 'end']:
        return 1

    max_for_small_caves = 1 if special_used else 2
    return max_for_small_caves if node.islower() else 50


def _dfs(graph, visitation, current, end_node, special_used):
    # End of route? Count it as 1
    if current == end_node:
        return 1

    # Invalid move (already visited small cave)? Don't count it
    # Also added a safety check for big caves to avoid infinite loops
    max_visits = 1 if current.islower() else 50
    if visitation[current] >= get_limit(current, special_used):
        return 0

    # Neither of the above?
    # Mark this cave as visited
    # Count the number of paths that continue through each neighbor and add them up
    visitation[current] += 1
    if visitation[current] > 1 and current.islower():
        special_used = True

    return sum([_dfs(graph, visitation.copy(), neighbor, end_node, special_used) for neighbor in graph[current]])


def dfs(graph, special_used):
    visitation = dict(list(zip(input.keys(), repeat(0))))
    return _dfs(graph, visitation, 'start', 'end', special_used)

def part_1(input):
    print(f'Part 1: Distinct paths #: {dfs(input, True)}')

def part_2(input):
    print(f'Part 1: Distinct paths #: {dfs(input, False)}')


input = read_input()
part_1(input)
part_2(input)


