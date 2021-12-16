#!/usr/bin/env python3

def read_input():
    with open('./input.txt', 'r') as input_file:
        return [int(x) for x in input_file.readlines()]

def part_1(input, output_prefix):
    result = sum([1 if d1 < d2 else 0 for (d1, d2) in zip(input[:-1], input[1:])])
    print(f'{output_prefix} result: {result}')

def part_2(input):
    input = [sum(input[i:i+3]) for i in range(0, len(input)-2)]
    part_1(input, "Part 2")

input = read_input()
part_1(input, "Part 1")
part_2(input)
