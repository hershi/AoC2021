#!/usr/bin/env python3

from enum import Enum

class Board:
    def __init__(self, text, board_name):
        self.items = list(map(lambda x: [int(x), False], " ".join(text).split()))
        self.board_name = board_name
        self.won = False

    def process(self, x):
        for (i, e) in enumerate(self.items):
            if e[0] == x:
                e[1] = True
                return self.check_board(i, x)

        return (False, None)

    def get_row(self, r):
        return [self.items[r*5+i] for i in range(5)]

    def get_col(self, c):
        return [self.items[c+5*i] for i in range(5)]

    def check_board(self, i, num):
        win = all(map(lambda x: x[1], self.get_row(i//5))) or all(map(lambda x: x[1], self.get_col(i%5)))
        if not win:
            return (False, None)

        score = sum([e[0] for e in self.items if not e[1]]) * num
        self.won = True
        return (True, score)


def read_input():
    with open('./input.txt', 'r') as input_file:
        numbers = [int(x) for x in input_file.readline().strip().split(",")]

        boards = []
        while(True):
            if not input_file.readline():
                return numbers, boards

            boards.append(Board([input_file.readline().strip() for i in range(5)], len(boards)))



def part_1(numbers, boards):
    for n in numbers:
        print(f'Processing {n}')
        for b in boards:
            (won, score) = b.process(n)
            if won:
                print(f'Board {b.board_name} won with score {score}')
                return


def part_2(numbers, boards):
    for n in numbers:
        for b in boards:
            if b.won:
                continue

            (won, score) = b.process(n)
            if won:
                print(f'Board {b.board_name} won with score {score}')

numbers, boards = read_input()
# part_1(numbers, boards[0:1])
part_1(numbers, boards)
part_2(numbers, boards)


