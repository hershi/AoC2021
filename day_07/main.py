#!/usr/bin/env python3

def read_input():
    with open('./input.txt', 'r') as input_file:
        return [int(p) for p in input_file.readline().strip().split(",")]


def fuel_needed(input, pos):
    return sum([abs(p-pos) for p in input])

def fuel_needed_v2(input, pos):
    return sum([(1 + abs(p-pos))*abs(p-pos) // 2 for p in input])

def part_1(input):
    lower = min(input)
    upper = max(input)

    while(True):
        pivot = (lower + upper) // 2
        lower_fuel = fuel_needed(input, lower)
        upper_fuel = fuel_needed(input, upper)

        if abs(upper-lower) <= 1:
            if upper_fuel < lower_fuel:
                print(f'Part 1: Fuel needed {upper_fuel} (position {upper})')
            else:
                print(f'Part 1: Fuel needed {lower_fuel} (position {lower})')
            return

        if  upper_fuel > lower_fuel:
            upper = pivot
        else:
            lower = pivot


def part_2(input):
    lower = min(input)
    upper = max(input)

    while(True):
        pivot = (lower + upper) // 2
        lower_fuel = fuel_needed_v2(input, lower)
        upper_fuel = fuel_needed_v2(input, upper)

        if abs(upper-lower) <= 1:
            if upper_fuel < lower_fuel:
                print(f'Part 1: Fuel needed {upper_fuel} (position {upper})')
            else:
                print(f'Part 1: Fuel needed {lower_fuel} (position {lower})')
            return

        if  upper_fuel > lower_fuel:
            upper = pivot
        else:
            lower = pivot


input = read_input()
part_1(input)
part_2(input)


