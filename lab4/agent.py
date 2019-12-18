import random

from lab1.utils import Position
from lab4.choices import ANY, GOLD, VIY, P_VIY, EMPTY, LADY, P_LADY, WALL, SAFE
from lab4.map import Map


class Agent:
    def __init__(self, map: Map):
        self.world_map = map
        self.agent_map = self.get_agent_map()
        # position
        self.x = 1
        self.y = 1

        self.world_map.agent_pos = Position(self.x, self.y)
        self.agent_map.agent_pos = Position(self.x, self.y)
        self.can_kick = True

    @classmethod
    def get_agent_map(cls):
        map = Map.get_empty_map()
        for i in range(1, len(map) - 1):
            for j in range(1, len(map[0]) - 1):
                map[i][j] = ANY
        return Map(map)

    @property
    def pos(self):
        return Position(self.x, self.y)

    def update_map(self):
        """
        Analizes agent's sensors and updates map
        """
        self.agent_map[self.pos] = self.world_map[self.pos]
        self.update_positions(self.check_pos(Position(self.x + 1, self.y)))
        self.update_positions(self.check_pos(Position(self.x - 1, self.y)))
        self.update_positions(self.check_pos(Position(self.x, self.y + 1)))
        self.update_positions(self.check_pos(Position(self.x, self.y - 1)))

    def update_pos(self, pos, item):
        # if item == ANY and self.agent_map[pos] != WALL and self.agent_map[
        #     pos] != EMPTY:
        #     self.agent_map[pos] = SAFE
        if self.agent_map[pos] == ANY:
            self.agent_map[pos] = item
        elif self.agent_map[pos] == P_VIY and item == P_VIY:
            self.agent_map[pos] = VIY

    def update_positions(self, item):
        self.update_pos(Position(self.x + 1, self.y), item)
        self.update_pos(Position(self.x - 1, self.y), item)
        self.update_pos(Position(self.x, self.y + 1), item)
        self.update_pos(Position(self.x, self.y - 1), item)

    def check_pos(self, pos):
        """
        Analizes position on world map and returns item for agent map
        """
        item = self.world_map[pos]
        if item == VIY:
            return P_VIY
        elif item == LADY:
            return P_LADY
        else:
            return ANY

    def is_safe_pos(self, pos):
        return self.agent_map[pos] != P_LADY and self.agent_map[
            pos] != P_VIY and (self.agent_map[pos] != VIY or self.agent_map[
            pos] == VIY and self.can_kick)

    def is_available_pos(self, pos):
        return self.is_safe_pos(pos) and self.agent_map[pos] != WALL

    def get_available_moves(self):
        moves = []

        def check_move(pos):
            if self.is_available_pos(pos):
                moves.append(pos)

        check_move(Position(self.x + 1, self.y))
        check_move(Position(self.x - 1, self.y))
        check_move(Position(self.x, self.y + 1))
        check_move(Position(self.x, self.y - 1))
        return moves

    def get_best_moves(self, moves):
        best = []
        for pos in moves:
            if self.agent_map[pos] in {ANY, SAFE}:
                best.append(pos)
            elif self.agent_map[pos] == VIY:
                return [pos]
        return best

    def move(self, pos):
        self.x = pos.x
        self.y = pos.y
        self.world_map.agent_pos = Position(self.x, self.y)
        self.agent_map.agent_pos = Position(self.x, self.y)

    def kick(self, pos):
        if self.world_map[pos] == VIY:
            self.world_map[pos] = EMPTY
            for i in range(self.agent_map.map_size.height):
                for j in range(self.agent_map.map_size.width):
                    if self.agent_map[Position(i, j)] == P_VIY:
                        self.agent_map[Position(i, j)] = ANY
                    elif self.agent_map[Position(i, j)] == VIY:
                        self.agent_map[Position(i, j)] = SAFE
            print('VIY KILLED')
        self.can_kick = False

    def act(self):
        if self.agent_map[self.pos] == GOLD:
            print('GOLD COLLECTED')
            return True
        else:
            available_moves = self.get_available_moves()
            if not available_moves:
                print('GAME OVER')
                return True
            else:
                best_moves = self.get_best_moves(available_moves)
                if best_moves:
                    # print(best_moves)
                    # print([self.agent_map[pos] for pos in best_moves])
                    pos = random.choice(best_moves)
                    if self.agent_map[pos] == VIY:
                        self.kick(pos)
                    else:
                        self.move(pos)
                else:
                    self.move(random.choice(available_moves))

    def go(self, iters):
        for _ in range(iters):
            self.update_map()
            self.print_maps()
            if self.act():
                return

    def print_maps(self):
        agent = self.agent_map.__str__().split('\n')
        world = self.world_map.__str__().split('\n')
        for i in range(len(agent)):
            print(world[i], ' ' * 3, agent[i])
