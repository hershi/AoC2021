#!/usr/bin/env python3

def read_input():
    with open('./input.txt', 'r') as input_file:
        fish = {}
        for f in map(lambda x: int(x), input_file.readline().strip().split(",")):
            fish[f] = fish.get(f, 0)+1

        return fish


def calc(input, days):
    fish = input.copy()
    for i in range(days):
        # print (f'Day {i}: {sum(fish.values())}; {fish}')
        zeros = fish.get(0, 0)
        fish = {(f-1): c for (f,c) in fish.items() if f > 0}
        fish[6] = fish.get(6,0) + zeros
        fish[8] = fish.get(8,0) + zeros

    return sum(fish.values())


def part_1(input):
    days = 80
    print(f"Part 1: After {days} days there'll be {calc(input, days)}")


def part_2(input):
    days = 256
    print(f"Part 2: After {days} days there'll be {calc(input, days)}")


input = read_input()
part_1(input)
part_2(input)


