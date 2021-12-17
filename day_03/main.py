#!/usr/bin/env python3

from enum import Enum

def read_input():
    with open('./input.txt', 'r') as input_file:
        return input_file.readlines()

def part_1(input):
    gamma = 0
    epsilon = 0
    for i in range(len(input[0])-1):
        s = sum([int(l[i]) for l in input]) > (len(input)/2)
        gamma = gamma * 2 + s
        epsilon = epsilon * 2 + (1-s)

    print(f'Gamma {gamma}, Epsilon {epsilon}, Gamme*Epsilon {gamma*epsilon}')


class RatingType(Enum):
    OXYGEN_GENERATOR = 1
    CO2_SCRUBBING = 0


def _part_2_filter(input, i, rating_type):
    if len(input) <= 1:
        return input[0]

    if sum([int(entry[i]) for entry in input]) >= len(input)/2:
        keep = rating_type.value
    else:
        keep = 1 - rating_type.value

    return _part_2_filter(list(filter(lambda e: int(e[i]) == keep, input)), i+1, rating_type)

def part_2(input):
    oxygen_generator_rating = int(_part_2_filter(input, 0, RatingType.OXYGEN_GENERATOR), base=2)
    co2_scrubbing_rating = int(_part_2_filter(input, 0, RatingType.CO2_SCRUBBING), base=2)
    print(f'Oxy: {oxygen_generator_rating} CO2: {co2_scrubbing_rating} result: {oxygen_generator_rating * co2_scrubbing_rating}')

input = read_input()
part_1(input)
part_2(input)


