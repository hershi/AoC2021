#!/usr/bin/env python3

from itertools import chain
from collections import Counter

DECODER = {
    'abcefg': 0,
    'cf': 1,
    'acdeg': 2,
    'acdfg': 3,
    'bcdf': 4,
    'abdfg': 5,
    'abdefg': 6,
    'acf': 7,
    'abcdefg': 8,
    'abcdfg': 9,
}


def read_input():
    result = []
    with open('./input.txt', 'r') as input_file:
        for l in input_file.readlines():
            observations, outputs = l.strip().split(" | ")
            observations = observations.strip().split()
            outputs = outputs.strip().split()
            result.append((observations, outputs))

        return result

def part_1(input):
    interesting = set([2,3,4,7])
    print(
        len(
        list(
        filter(lambda x: len(x) in interesting,
        chain.from_iterable(
        map(lambda x: x[1], input)
    )))))


def decode(output, translations):
    return DECODER["".join(sorted([translations[l] for l in output]))]


def solve(observations, outputs):
    observation_counts = {}

    line_counter = Counter(chain.from_iterable(observations))

    frequency_counts = {
        v: k for (k,v) in line_counter.items() if v not in [7,8]
    }

    translations = {
        frequency_counts[6] : 'b',
        frequency_counts[4] : 'e',
        frequency_counts[9] : 'f',
    }

    # Find the 'c' line. Search for the '1' observation, then find which of the
    # two signals connects to the 'f' segment, and the remaining one is 'c'
    one_observation = filter(lambda x: len(x) == 2, observations).__next__()
    c_line = [c for c in one_observation if c not in translations][0]
    translations[c_line] = 'c'

    # The 'a' line is the remaining signal that has 8 occurences
    a_line = [k for k in line_counter.keys() if line_counter[k] == 8 and k not in translations][0]
    translations[a_line] = 'a'

    four_observation = filter(lambda x: len(x) == 4, observations).__next__()
    d_line = [c for c in four_observation if c not in translations][0]
    translations[d_line] = 'd'

    g_line = [k for k in line_counter.keys() if line_counter[k] == 7 and k not in translations][0]
    translations[g_line] = 'g'

    return int("".join([f'{decode(o, translations)}' for o in outputs]))


def part_2(input):
    s = 0
    for i in input:
        s += solve(*i)

    print(f'Part 2 solution: {s}')


input = read_input()
part_1(input)
part_2(input)


