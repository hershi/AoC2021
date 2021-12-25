#!/usr/bin/env python3

class Grid:
    def __init__(self, values, width):
        self.values = values
        self.width = width
        self.height = len(values) // width

    def get(self, x,y):
        return self.values[x + y*self.width]


    def set(self, x, y, val):
        self.values[x + y*self.width] = val


    def increment(self, x, y):
        self.values[x + y*self.width] += 1


    def neighbors(self, x,y):
        return list(filter(lambda c: self._valid_coordinates(*c),
               [
                   (x+1, y),
                   (x-1, y),
                   (x, y+1),
                   (x, y-1),
                   (x-1, y-1),
                   (x-1, y+1),
                   (x+1, y-1),
                   (x+1, y+1),
               ]
        ))


    def clone(self):
        return Grid(self.values[:], self.width)


    def _valid_coordinates(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height


    def step(self):
        self.values = [v+1 for v in self.values]

        flashed = set()
        to_check = set([(x,y) for x in range(self.width) for y in range(self.height)])

        while to_check:
            x,y = to_check.pop()

            if (x,y) in flashed:
                continue

            if self.get(x,y) <= 9:
                continue

            flashed.add((x,y))

            for nx,ny in self.neighbors(x,y):
                self.increment(nx,ny)
                to_check.add((nx,ny))



        for x,y in flashed:
            self.set(x,y,0)

        return len(flashed)


    def __repr__(self):
        res = ""
        for l in zip(*[iter(self.values)]*self.width):
            res += "".join(str(d) for d in l) + "\n"

        return res


    class Iterator:
        def __init__(self, values):
            self.values = values
            self.i = 0


        def __next__(self):
            if self.i >= len(self.values):
                raise StopIteration

            self.i += 1
            return self.values[self.i - 1]

    def __iter__(self):
        return Grid.Iterator(self.values)



def read_input():
    with open('./input.txt', 'r') as input_file:
        lines = input_file.readlines()
        width = len(lines[0].strip())
        values = [int(d) for line in lines for d in line.strip()]
        return Grid(values, width)


def part_1(input):
    flashes = [input.step() for i in range(100)]
    print(f'Part 1: {sum(flashes)} ({flashes})')


def part_2(input):
    steps = 1000000
    for i in range(steps):
        if input.step() == 100:
            print(f'All octopi flashed together - step {i + 1}')
            return

    print(f'No step where all octopi flashes in the first {steps} steps')


input = read_input()
part_1(input.clone())
part_2(input)


