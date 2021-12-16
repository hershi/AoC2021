#!/usr/bin/env python3

import numpy as np

COMMANDS = {
    'forward': np.array([1,0]),
    'up': np.array([0,-1]),
    'down': np.array([0,1]),
}

def read_input():
    with open('./input.txt', 'r') as input_file:
        input = [l.split() for l in input_file.readlines()]
        return [(c,int(m)) for (c,m) in input]

def part_1(input):
    input = [COMMANDS[item[0]] * int(item[1]) for item in input]
    endpoint = sum(input)
    print(f'{endpoint} : {endpoint[0] * endpoint[1]}')

def part_2(input):
    aim = 0
    pos = np.array([0,0])
    for (c, m) in input:
        if c == 'forward':
            pos += np.array([m, aim*m])
        elif c == 'up':
            aim -= m
        else: # down
            aim += m

    print(f'{pos} : {pos[0] * pos[1]}')

input = read_input()
part_1(input)
part_2(input)

