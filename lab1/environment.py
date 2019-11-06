import os
from random import randint

from lab1 import choices
from lab1.utils import Size, Position


class Environment:
    def __init__(self, map_path, size: Size = Size(12, 12)):
        self.size = size
        self.map = self.read_map(map_path)
        self.agents = []

    @classmethod
    def read_map(cls, path):
        dirname = os.path.dirname(__file__)
        abs_path = os.path.join(dirname, path)
        with open(abs_path, 'r') as f:
            raw_map = f.readlines()
        map = []
        for line in raw_map:
            map.append(list(line[:-1]))
        return map

    def add_garbage(self):
        while True:
            x, y = randint(1, self.size.len - 1), randint(1,
                                                          self.size.width - 1)
            if self.map[x][y] != choices.WALL:
                self.map[x][y] = choices.GARBAGE
                break

    def clean_garbage(self, pos: Position):
        self.map[pos.x][pos.y] = choices.EMPTY

    def check_garbage(self, pos: Position):
        return self.map[pos.x][pos.y] == choices.GARBAGE

    def check_cell(self, pos: Position):
        return self.map[pos.x][pos.y] != choices.WALL

    def get_garbage_sum(self):
        sum_ = 0
        for i in range(self.size.len):
            for j in range(self.size.width):
                if self.map[i][j] == choices.GARBAGE:
                    sum_ += 1
        return sum_

    def run(self, iterations, agent):
        total_garbage_sum = 0
        for _ in range(iterations):
            self.add_garbage()
            agent.act()
            total_garbage_sum += self.get_garbage_sum()
        return total_garbage_sum / iterations, agent.used_energy




