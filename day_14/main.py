#!/usr/bin/env python3
import re
from collections import Counter
from itertools import (
    chain,
    repeat,
    zip_longest
)

def read_input():
    with open('./input.txt', 'r') as input_file:
        lines = input_file.readlines()

    template = lines[0].strip()
    rules = {x[0]: x[1] for x in [line.strip().split(' -> ') for line in lines[2:]]}
    return template, rules


def do_insertions(template, rules):
    insertions = [rules.get(f'{c1}{c2}', '') for c1,c2 in zip(iter(template), iter(template[1:]))]
    return ''.join([f'{s1}{s2}' for s1,s2 in zip_longest(iter(template), iter(insertions), fillvalue='')])


def part_1(template, rules):
    for i in range(10):
        template = do_insertions(template, rules)

    frequency = Counter(template).most_common()
    print(f'Part 1 solution: {frequency[0][1] - frequency[-1][1]}')
    print(f'Most and least common: {frequency[0]} {frequency[-1]}')

def part_2(template, rules):
    substitution_rules = {k: [f'{k[0]}{v}', f'{v}{k[1]}'] for k,v in rules.items()}
    pairs = Counter([f'{c1}{c2}' for c1,c2 in zip(iter(template), iter(template[1:]))])
    for i in range(40):
        pr = {}
        for p, c in pairs.items():
            keys = substitution_rules.get(p, p)
            for k in keys:
                pr[k] = pr.get(k, 0) + c

        pairs = pr

    frequency = {}
    for k,v in pairs.items():
        frequency[k[0]] = frequency.get(k[0], 0) + v
        frequency[k[1]] = frequency.get(k[1], 0) + v

    frequency = sorted([(k,(v+1)//2) for k,v in frequency.items()], key=lambda x: x[1])
    print(frequency[-1][1] - frequency[0][1])


template,rules = read_input()
part_1(template, rules)
part_2(template, rules)


