import random

from lab1 import choices
from lab1.environment import Environment
from lab1.utils import Position, energy_required, Node


class Agent:
    def __init__(self, environment: Environment, position: Position):
        self.pos = position
        self.env = environment
        self.used_energy = 0
        self.garbage_colected = 0

    @energy_required(energy=1)
    def _move(self, pos: Position):
        if self.env.check_cell(pos):
            self.pos = pos

    def go_left(self):
        self._move(Position(self.pos.x - 1, self.pos.y))

    def go_right(self):
        self._move(Position(self.pos.x + 1, self.pos.y))

    def go_top(self):
        self._move(Position(self.pos.x, self.pos.y + 1))

    def go_bottom(self):
        self._move(Position(self.pos.x, self.pos.y - 1))

    @energy_required(energy=2)
    def do_clean(self):
        self.env.clean_garbage(self.pos)

    def do_nothing(self):
        pass

    def act(self):
        raise NotImplementedError


class RandomAgent(Agent):
    def __init__(self, *args, **kwargs):
        self.actions = [self.go_left, self.go_right, self.go_bottom,
                        self.go_top, self.do_clean, self.do_nothing]
        super().__init__(*args, **kwargs)

    def act(self):
        random.choice(self.actions)()


class ReflectiveAgent(Agent):
    def __init__(self, *args, **kwargs):
        self.prev_pos = None
        super().__init__(*args, **kwargs)

    def get_moves(self, check_func):
        moves = []
        if check_func(Position(self.pos.x - 1, self.pos.y)):
            moves.append(self.go_left)
        if check_func(Position(self.pos.x + 1, self.pos.y)):
            moves.append(self.go_right)
        if check_func(Position(self.pos.x, self.pos.y - 1)):
            moves.append(self.go_bottom)
        if check_func(Position(self.pos.x, self.pos.y + 1)):
            moves.append(self.go_top)
        return moves

    def get_available_moves(self):
        return self.get_moves(self.env.check_cell)

    def get_efective_moves(self):
        return self.get_moves(self.env.check_garbage)

    def act(self):
        if self.env.check_garbage(self.pos):
            self.do_clean()
        else:
            efective_moves = self.get_efective_moves()
            all_moves = self.get_available_moves()
            random.choice(
                efective_moves)() if efective_moves else random.choice(
                all_moves)()


class ModelBasedAgent(Agent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.map = self.build_map()
        self.temp_map = None
        self.cur_step = 1

    def move(self, pos: Position):
        self.map[pos.x][pos.y] = self.cur_step
        self._move(pos)
        self.cur_step += 1

    def get_moves(self, check_func):
        moves = []
        if check_func(Position(self.pos.x - 1, self.pos.y)):
            moves.append(self.go_left)
        if check_func(Position(self.pos.x + 1, self.pos.y)):
            moves.append(self.go_right)
        if check_func(Position(self.pos.x, self.pos.y - 1)):
            moves.append(self.go_bottom)
        if check_func(Position(self.pos.x, self.pos.y + 1)):
            moves.append(self.go_top)
        return moves

    def get_efective_moves(self):
        return self.get_moves(self.env.check_garbage)

    def build_map(self):
        map = []
        for row in self.env.map:
            map.append([])
            for cell in row:
                if cell == choices.WALL:
                    map[-1].append(float('inf'))
                else:
                    map[-1].append(0)
        return map

    def get_min_pos(self):
        min_pos = Position(0, 0)
        for i in range(len(self.map)):
            for j in range(len(self.map[i])):
                if self.map[i][j] < self.map[min_pos.x][min_pos.y] and self.pos.x != i and self.pos.y != j:
                    min_pos = Position(i, j)
        return min_pos

    def dp(self, node: Node, temp_matrix: list):
        cur_node = temp_matrix[node.pos.x][node.pos.y]
        if cur_node.total_weight / cur_node.count > node.total_weight / node.count:
            node.visited = True
            temp_matrix[node.pos.x][node.pos.y] = node
        positions = (Position(node.pos.x - 1, node.pos.y),
                     Position(node.pos.x + 1, node.pos.y),
                     Position(node.pos.x, node.pos.y - 1),
                     Position(node.pos.x, node.pos.y + 1))
        for pos in positions:
            if not temp_matrix[pos.x][pos.y].visited:
                new_node = Node(from_node=node,
                             count=node.count + 1,
                             total_weight=node.total_weight + self.map[pos.x][
                                 pos.y],
                             pos=pos)
                self.dp(new_node,
                        temp_matrix)


    def build_temp_matrix(self):
        temp = []
        for i in range(len(self.map)):
            temp.append([])
            for j in range(len(self.map[i])):
                node = Node()
                if not self.env.check_cell(Position(i, j)):
                    node.visited = True
                temp[-1].append(node)
        return temp

    def get_best_path(self):
        min_pos = self.get_min_pos()
        min_node = Node(pos=min_pos,
                        total_weight=self.map[min_pos.x][min_pos.y],
                        visited=True)

        temp_map = self.build_temp_matrix()
        temp_map[min_pos.x][min_pos.y] = min_node
        self.dp(min_node, temp_map)
        self.temp_map = temp_map

    def act(self):
        if self.env.check_garbage(self.pos):
            self.do_clean()
        else:
            efective_moves = self.get_efective_moves()
            if efective_moves:
                random.choice(efective_moves)()
            else:
                if not self.temp_map or self.temp_map and not \
                self.temp_map[self.pos.x][self.pos.y].from_node:
                    self.get_best_path()
                self._move(self.temp_map[self.pos.x][self.pos.y].from_node.pos)

