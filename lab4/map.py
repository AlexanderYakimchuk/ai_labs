from random import randint

from lab1.utils import Position
from lab4.utils import Size
from lab4.choices import WALL, EMPTY, LADY, GOLD, VIY, ANY, AGENT


class Map:
    map_size = Size(4, 6)
    ladies = 1
    gold = 2

    def __init__(self, map=None):
        self.map = map or self.get_random_map()
        self.agent_pos = None

    @classmethod
    def get_empty_map(cls):
        map = []
        map.append([WALL] * (cls.map_size.width + 2))
        for _ in range(cls.map_size.height):
            map.append([WALL] + [EMPTY] * cls.map_size.width + [WALL])
        map.append([WALL] * (cls.map_size.width + 2))
        return map

    @classmethod
    def get_random_map(cls):
        map = cls.get_empty_map()
        map[1][1] = WALL  # reserve room for agent
        cls.add_item(map, VIY)
        for _ in range(cls.ladies):
            cls.add_item(map, LADY)
        for _ in range(cls.gold):
            cls.add_item(map, GOLD)
        map[1][1] = EMPTY  # release reserved room
        return map

    @classmethod
    def add_item(cls, map, item):
        while True:
            x = randint(1, cls.map_size.height)
            y = randint(1, cls.map_size.width)
            if map[x][y] == EMPTY:
                map[x][y] = item
                return

    def __getitem__(self, pos: Position):
        return self.map[pos.x][pos.y]

    def __setitem__(self, pos: Position, item):
        self.map[pos.x][pos.y] = item

    def __str__(self):
        item = self[self.agent_pos]
        self[self.agent_pos] = AGENT
        str = ''
        for i in range(self.map_size.height + 2):
            str += ''.join([' '.join(x for x in self.map[i]), '\n'])
        self[self.agent_pos] = item
        return str

    def __repr__(self):
        return self.__str__()
