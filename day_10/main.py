#!/usr/bin/env python3

from collections import Counter


COMPLETION_SCORING = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}


SYNTAX_SCORING = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}


CLOSER_MAPPING = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

def read_input():
    with open('./input.txt', 'r') as input_file:
        return [l.strip() for l in input_file.readlines()]


def process_line(line):
    expected_closers = []
    for c in line:
        if c in CLOSER_MAPPING.keys():
            expected_closers.append(CLOSER_MAPPING[c])
            continue

        if expected_closers[-1] != c:
            return False, c

        expected_closers.pop()

    return True, expected_closers


def get_first_illegal_closer(line):
    processing_result = process_line(line)
    return None if processing_result[0] else processing_result[1]


def part_1(input):
    illegal_closers = [get_first_illegal_closer(l) for l in input]
    score = sum([SYNTAX_SCORING[c] for c in illegal_closers if c])
    print(f'The total score is {score} ({illegal_closers})')


def calc_completion_score(completion):
    score = 0
    for c in completion:
        score = score * 5 + COMPLETION_SCORING[c]

    return score


def part_2(input):
    incomplete_lines = [reversed(x[1]) for x in [process_line(l) for l in input] if x[0]]
    scores = sorted([calc_completion_score(x) for x in incomplete_lines])
    print(f'The score for complteion is {scores[len(scores)//2]} ({scores})')


input = read_input()
part_1(input)
part_2(input)


